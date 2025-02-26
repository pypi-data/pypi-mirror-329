import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.canvasapirc")

def setup_config_file():
    api_url = input('enter your canvas url (e.g. https://canvas.instructure.com): ')
    api_key = input('enter your canvas api key: ')

    with open(CONFIG_PATH, 'w') as f:
        f.write("[DEFAULT]\n")
        f.write(f"API_URL = {api_url}\n")
        f.write(f"API_KEY = {api_key}\n")
    return api_key, api_url

def load_api_info():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
        api_key = config.get("DEFAULT", "API_KEY", fallback=None)
        api_url = config.get("DEFAULT", "API_URL", fallback=None)
                    
        return api_key, api_url

    else:
        return setup_config_file()

API_KEY, API_URL = load_api_info()