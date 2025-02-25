from importlib import import_module
from importlib.util import find_spec

from plain.packages import PackageConfig, packages_registry

MODELS_MODULE_NAME = "models"


class Config(PackageConfig):
    name = "plain.models"
    # We want to use the "migrations" module
    # in this package but not for the standard purpose
    migrations_module = None

    def ready(self):
        # Trigger register calls to fire by importing the modules
        for package_config in packages_registry.get_package_configs():
            module_name = f"{package_config.name}.{MODELS_MODULE_NAME}"
            if find_spec(module_name):
                import_module(module_name)
