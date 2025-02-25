from ..fpcli_settings import CONFIG_FOLDER
import importlib.util

def get_settings():
    # Dynamically import settings
    settings_path = f"{CONFIG_FOLDER}.settings"
    spec = importlib.util.find_spec(settings_path)
    if spec is None:
        raise ImportError(f"Settings module not found in {CONFIG_FOLDER}")

    settings = importlib.import_module(settings_path)
    return settings.Settings()

def get_settings_class():
    # Dynamically import settings
    settings_path = f"{CONFIG_FOLDER}.settings"
    spec = importlib.util.find_spec(settings_path)
    if spec is None:
        raise ImportError(f"Settings module not found in {CONFIG_FOLDER}")

    settings = importlib.import_module(settings_path)
    return settings