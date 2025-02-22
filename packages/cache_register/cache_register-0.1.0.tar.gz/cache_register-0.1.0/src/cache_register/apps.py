import importlib

from django.apps import AppConfig
from django.conf import settings

from .register import _global_dict_register


class CacheRegisterConfig(AppConfig):  # type: ignore [misc]
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cache_register'


for app in settings.INSTALLED_APPS:
    try:
        importlib.import_module(f"{app}.registers")
    except ModuleNotFoundError:
        pass

    for register in _global_dict_register:
        try:
            importlib.import_module(f"{app}.{register}")
        except ModuleNotFoundError:
            pass

