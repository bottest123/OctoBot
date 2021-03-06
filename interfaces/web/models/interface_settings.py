import copy

from interfaces import get_bot
from config.cst import CONFIG_WATCHED_SYMBOLS, CONFIG_FILE, TEMP_RESTORE_CONFIG_FILE, CONFIG_CRYPTO_CURRENCIES, \
    CONFIG_CRYPTO_PAIRS
from tools.config_manager import ConfigManager


def _get_config():
    return get_bot().get_edited_config()


def _symbol_in_currencies_config(config, symbol):
    for crypto_currency_data in config[CONFIG_CRYPTO_CURRENCIES].values():
        if symbol in crypto_currency_data[CONFIG_CRYPTO_PAIRS]:
            return True
    return False


def get_watched_symbols():
    config = _get_config()
    if CONFIG_WATCHED_SYMBOLS not in config:
        config[CONFIG_WATCHED_SYMBOLS] = []
    else:
        for symbol in copy.copy(config[CONFIG_WATCHED_SYMBOLS]):
            if not _symbol_in_currencies_config(config, symbol):
                config[CONFIG_WATCHED_SYMBOLS].remove(symbol)
    return config[CONFIG_WATCHED_SYMBOLS]


def add_watched_symbol(symbol):
    watched_symbols = get_watched_symbols()
    watched_symbols.append(symbol)
    return _save_edition()


def remove_watched_symbol(symbol):
    watched_symbols = get_watched_symbols()
    if symbol in watched_symbols:
        watched_symbols.remove(symbol)
    return _save_edition()


def _save_edition():
    to_save_config = copy.copy(_get_config())
    ConfigManager.remove_loaded_only_element(to_save_config)
    ConfigManager.save_config(CONFIG_FILE, to_save_config, TEMP_RESTORE_CONFIG_FILE)
    return True
