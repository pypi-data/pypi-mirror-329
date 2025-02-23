"""
Configuration module based on tiangolo implementation of `pydantic_settings`.
Custom implementation by Artemis Resende <artemis@aresende.com>

Source: https://github.com/fastapi/full-stack-fastapi-template/blob/d2020c1a37efd368afee4d3e56897fc846614f80/backend/app/core/config.py
Licensed under MIT
"""

from pathlib import Path
from typing import Annotated, Any

from fastapi_mail import ConnectionConfig
from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    model_validator, EmailStr, SecretStr, PrivateAttr, field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from commons.db import DatabaseAdapter
from commons.net import IPV4_LOOPBACK
from webserver import env


def _parse_str_list(str_list: Any) -> list[str] | str:
    """
    Parse a string list of elements separated by commas.

    :param str_list:
    :return: a list with all cors origins
    """
    if isinstance(str_list, str) and not str_list.startswith("["):
        return [i.strip() for i in str_list.split(",")]
    elif isinstance(str_list, list | str):
        return str_list
    raise ValueError(str_list)


class Settings(BaseSettings):
    # "Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0.
    # See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.10/migration/"
    model_config = SettingsConfigDict(
        env_file=f"{env.root()}/.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_NAME: str = "fastapi.webserver"
    ENVIRONMENT: env.Environment = "local"

    RESOURCES_FOLDER: Path | str = env.root()  # TODO: find another way to resolve root because may trigger some issues

    @staticmethod
    @field_validator("RESOURCES_FOLDER")
    def validate_required_path(v: str):
        if Path(v).exists():
            return v

        raise ValueError(f"'{v}' does not exists.")

    @computed_field
    @property
    def resources_folder(self) -> Path:
        return Path(self.RESOURCES_FOLDER)

    # --- HTTP  ---
    HTTP_ROOT_PATH: str = '/'                  # it must start with a '/'
    STATIC_FOLDER: str = ""                    # Enables `{HTTP_ROOT_PATH}/static`; Should be relative to RESOURCES_PATH and not start with a '/'
    HOST: str = IPV4_LOOPBACK
    PORT: int = 8000
    ENABLE_SSL: bool = False
    SSL_CERTIFICATE: str = ""
    SSL_PRIVATE_KEY: str = ""
    CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(_parse_str_list)
    ] = []  # string list separated by commas

    @computed_field
    @property
    def enable_ssl(self) -> bool:
        return bool((self.SSL_CERTIFICATE and self.SSL_PRIVATE_KEY) or self.ENABLE_SSL)

    @staticmethod
    @field_validator("SSL_CERTIFICATE", "SSL_PRIVATE_KEY")
    def validate_optional_path(v: str):
        if not v or Path(v).exists():
            return v

        raise ValueError(f"'{v}' does not exists.")

    @computed_field
    @property
    def http_static_enabled(self) -> bool:
        return bool(self.RESOURCES_FOLDER and self.STATIC_FOLDER)

    @computed_field
    @property
    def static_folder(self) -> Path | None:
        if self.http_static_enabled:
            return Path(f"{self.RESOURCES_FOLDER}/{self.STATIC_FOLDER}")

    @computed_field
    @property
    def ssl_certificate(self) -> Path | None:
        if self.SSL_CERTIFICATE:
            return Path(self.SSL_CERTIFICATE)

    @computed_field
    @property
    def ssl_private_key(self) -> Path | None:
        if self.SSL_PRIVATE_KEY:
            return Path(self.SSL_PRIVATE_KEY)

    # --- HTML Support / Templating ---
    TEMPLATES_FOLDER: str = ""                 # Enables HTML support for templating; Should be relative to RESOURCES_PATH and not start with a '/'

    @computed_field
    @property
    def templates_enabled(self) -> bool:
        return bool(self.RESOURCES_FOLDER and self.TEMPLATES_FOLDER)

    @computed_field
    @property
    def templates_folder(self) -> Path | None:
        if self.templates_enabled:
            return Path(f"{self.RESOURCES_FOLDER}/{self.TEMPLATES_FOLDER}")

    # --- Additional features ---
    MODULES: Annotated[
        list[str] | str, BeforeValidator(_parse_str_list)
    ] = []  # string list separated by commas

    # --- Keys ---
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8         # 60 minutes * 24 hours * 8 days = 8 days

    # --- Database ---
    _database_adapter: DatabaseAdapter | None = PrivateAttr(default=None)
    _cache_database_adapter: DatabaseAdapter | None = PrivateAttr(default=None)

    DB_ENGINE: str = ""
    DB_SERVER: str = ""
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str = ""

    @computed_field
    @property
    def has_database(self) -> bool:
        return bool(self.DB_ENGINE and self.DB_NAME)

    @computed_field
    @property
    def database_adapter(self) -> DatabaseAdapter:
        if self.has_database and not self._database_adapter:
            self._database_adapter = DatabaseAdapter(
                scheme=self.DB_ENGINE,
                host=self.DB_SERVER,
                port=self.DB_PORT,
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                database=f"{self.RESOURCES_FOLDER}/{self.DB_NAME}" if self.DB_ENGINE.startswith(
                    "sqlite") else self.DB_NAME
            )

        return self._database_adapter

    @computed_field
    @property
    def cache_database_adapter(self) -> DatabaseAdapter:
        if self.resources_folder and not self._cache_database_adapter:
            self._cache_database_adapter = DatabaseAdapter(
                scheme="sqlite",
                database=f"{self.resources_folder}/cache.db"
            )

        return self._cache_database_adapter

    # --- SMTP ---
    _smtp_config: ConnectionConfig | None = PrivateAttr(default=None)

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: SecretStr | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.APP_NAME
        return self

    @computed_field
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    @computed_field
    @property
    def smtp_config(self) -> ConnectionConfig:
        if not self._smtp_config:
            # build SMTP Config
            args: dict = {
                "MAIL_USERNAME": self.SMTP_USER,
                "MAIL_PASSWORD": self.SMTP_PASSWORD,
                "MAIL_FROM": self.EMAILS_FROM_EMAIL,
                "MAIL_PORT": self.SMTP_PORT,
                "MAIL_SERVER": self.SMTP_HOST,
                "MAIL_FROM_NAME": self.EMAILS_FROM_NAME,
                "MAIL_STARTTLS": True,
                "MAIL_SSL_TLS": False,
                "USE_CREDENTIALS": True,
            }

            if self.templates_enabled:
                args["TEMPLATE_FOLDER"] = self.templates_folder

            self._smtp_config = ConnectionConfig(**args)

        return self._smtp_config


# ------
settings: Settings = Settings()
