from datetime import datetime
from os import getcwd
from pathlib import Path
from subprocess import run
from sys import stdout
from typing import Any, Callable, Optional

from loguru import logger
from pydantic import ValidationError

from scriptman.core.config._manager import ConfigManager
from scriptman.core.config._toml import TOMLConfigManager
from scriptman.core.defaults import ConfigModel
from scriptman.core.version import Version


class Config:
    """
    📂 ConfigHandler Singleton Class

    Manages configuration, versioning, logging, and package management.
    """

    __initialized: bool = False
    __instance: Optional["Config"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "Config":
        """🔒 Singleton implementation ensuring a single instance."""
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(
        self, config: ConfigModel = ConfigModel(), version: Version = Version()
    ) -> None:
        """
        📝 Initialize configurations and create necessary directories.

        Args:
            config (ConfigModel): Configuration settings.
            version (Version): Version information.
        """
        if self.__initialized:
            return

        self.__version = version
        self.__cwd = Path(getcwd())
        self.__on_failure_callback: Optional[Callable[[Exception], None]] = None

        # Initialize config managers
        config_file = self._get_config_file_path()
        secrets_file = self._get_secrets_file_path()

        section = "scriptman" if "pyproject" in config_file.name else None
        self.__settings = TOMLConfigManager(config_file, section)
        self.__secrets = TOMLConfigManager(secrets_file)

        self._initialize_settings(config)
        self._initialize_logging()
        self.__initialized = True

    @property
    def cwd(self) -> Path:
        """
        📁 Retrieve the current working directory.

        Returns:
            Path: The current working directory.
        """
        return self.__cwd

    @property
    def version(self) -> str:
        """
        🎯 Retrieve the version information.

        Returns:
            str: The version information.
        """
        return str(self.__version)

    @property
    def scriptman(self) -> str:
        """
        🦸‍♂️ Retrieve the scriptman logo.

        Returns:
            str: The scriptman logo.
        """
        return self.__version.scriptman

    def _get_config_file_path(self) -> Path:
        """
        📁 Retrieve the path to the configuration file.

        Returns:
            Path: The path to the configuration file, prioritizing 'pyproject.toml' if it
            exists, otherwise 'scriptman.toml'.
        """
        if self.cwd.joinpath("pyproject.toml").exists():
            logger.debug("Using pyproject.toml")
            return self.cwd.joinpath("pyproject.toml")
        logger.debug("Using scriptman.toml")
        return self.cwd.joinpath("scriptman.toml")

    def _get_secrets_file_path(self) -> Path:
        """
        📂 Retrieve the path to the secrets file.

        Returns:
            Path: The path to the secrets file, or path of .secrets.toml file.
        """
        return self.cwd.joinpath(".secrets.toml")

    def _initialize_settings(self, config: ConfigModel) -> None:
        """
        📚 Initialize configuration defaults only for missing values.

        Iterate over the provided ConfigModel fields and set the default value in the
        config manager if the field is not already present.
        """
        for field_name, field in config.model_fields.items():
            if field_name not in self.__settings:
                self.__settings[field_name] = field.default

    def _initialize_logging(self) -> None:
        """📝 Initialize logging for the CLI handler."""
        logger.remove()  # FIXME: Logging before the handler is removed
        log_level = str(self.settings.get("log_level", "INFO"))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Console Handler
        logger.add(
            stdout,
            colorize=True,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<level>{message}</level>",
        )

        # File Handler
        logger.add(
            Path(str(self.settings.get("logs_dir", "logs"))) / f"{timestamp}.log",
            level=log_level,
            rotation="1 day",
            compression="zip",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
        )

    @property
    def settings(self) -> ConfigManager[dict[str, Any]]:
        return self.__settings

    @property
    def secrets(self) -> ConfigManager[dict[str, Any]]:
        return self.__secrets

    @property
    def on_failure_callback(self) -> Optional[Callable[[Exception], None]]:
        return self.__on_failure_callback

    def add_on_failure_callback_function(
        self, callback_function: Callable[[Exception], None]
    ) -> None:
        if not callable(callback_function):
            raise ValueError("Callback function must be callable")
        self.__on_failure_callback = callback_function

    def validate_and_update_configuration(self, param: str, value: Any) -> bool:
        """
        📝 Validates and updates a configuration parameter.

        Args:
            param (str): The parameter name to update.
            value (Any): The new value to set.

        Returns:
            bool: True if the configuration was updated successfully, False otherwise.
        """
        try:
            field = ConfigModel.model_fields[param]

            if field.annotation is bool and isinstance(value, str):
                value = value.lower() == "true"
            elif field.annotation is Path and isinstance(value, str):
                value = Path(value)
            elif field.annotation is not None:
                value = field.annotation(value)

            self.__settings.set(param.lower(), value, write_to_file=True)
            logger.info(f"Config updated successfully: {param} = {value}")
            return True
        except (KeyError, ValidationError, Exception) as e:
            logger.error(f"Failed to update configuration: {e}")
            return False

    def update_package(self, version: str = "latest") -> None:
        """📦 Update the scriptman package."""
        try:
            if version == "latest" or version == "next":
                major, minor, commit = [
                    int(v)
                    for v in str(self.__version.read_version_from_pyproject()).split(".")
                ]
                commit = self.__version.get_commit_count()
                commit += 1 if version == "next" else 0
            else:
                major, minor, commit = [int(v) for v in str(version).split(".")]
        except ValueError:
            raise ValueError(
                f'Invalid version format: "{version}" '
                "Please provide a valid major.minor.commit format with all integers."
            )

        self.__version.major, self.__version.minor, self.__version.commit = (
            major,
            minor,
            commit,
        )

        run(["poetry", "update"], check=True)
        self.__version.update_version_in_file("major", self.__version.major)
        self.__version.update_version_in_file("minor", self.__version.minor)
        self.__version.update_version_in_file("commit", self.__version.commit)
        run(["poetry", "version", str(self.version)])
        logger.info("📦 Package updated successfully")

    def publish_package(self) -> None:
        """📦 Publish the scriptman package to PyPI."""
        run(["poetry", "publish", "--build"], check=True)

    def lint(self) -> None:
        """⚡ Lint and typecheck the project files."""
        run(["isort", "."], check=True)
        run(["black", "."], check=True)
        run(["mypy", "."], check=True)


# Singleton instance
config: Config = Config()
__all__ = ["config"]
