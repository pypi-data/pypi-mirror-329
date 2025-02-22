
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

from wdg_core_file_storage.utils.file_util import format_lazy


USER_SETTINGS = getattr(settings, "WDG_CORE_FILE_STORAGE", None)

DEFAULTS = {
    "S3_ACCESS_KEY_ID": None,
    "S3_SECRET_ACCESS_KEY": None,
    "S3_BUCKET_NAME": "default-bucket",
    "S3_REGION": "us-east-1",
}


REMOVED_SETTINGS = (
    "AUTH_HEADER_TYPE",
    "AUTH_TOKEN_CLASS",
    "SECRET_KEY",
    "TOKEN_BACKEND_CLASS",
)


class APISettings(_APISettings):  # pragma: no cover
    def __check_user_settings(self, user_settings: dict[str, Any]) -> dict[str, Any]:
        SETTINGS_DOC = "https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html"

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    format_lazy(
                        _(
                            "The '{}' setting has been removed. Please refer to '{}' for available settings."
                        ),
                        setting,
                        SETTINGS_DOC,
                    )
                )

        return user_settings


api_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs) -> None:  # pragma: no cover
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "WDG_CORE_FILE_STORAGE":
        api_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)