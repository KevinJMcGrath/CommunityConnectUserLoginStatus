import jsonpickle

from pathlib import Path

from models.config import LogType

config_path = Path("config/config.json")

with open(config_path, 'r') as _config_file:
    _config = jsonpickle.decode(_config_file.read())

bot_config = _config['bot_config']
salesforce = _config['salesforce']


LogConfig = LogType(_config['logging'])


