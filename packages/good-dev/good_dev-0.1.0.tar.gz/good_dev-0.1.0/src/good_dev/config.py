import os
from pathlib import Path

from simple_toml_configurator import Configuration

CONFIG_DIR = Path(os.environ.get("GOOD_CONFIG_DIR", "~/.good-dev/")).expanduser()

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_DIR.joinpath("cache").mkdir(exist_ok=True)

# Define default configuration values
_default_config = {
    "secrets": {
        "scrapedo": "",
        "google_service_account": "",
    }
}

# Set environment variables
# os.environ["PROJECT_APP_UPLOAD_FOLDER"] = "overridden_uploads"

# Initialize the Simple TOML Configurator
settings = Configuration(
    config_path=CONFIG_DIR,
    defaults=_default_config,
    config_file_name="config",
    env_prefix="good",
)

settings.update()

# Creates an `app_config.toml` file in the `config` folder at the current working directory.

# # Access and update configuration values
# print(settings.app.ip)  # Output: '0.0.0.0'
# settings.app.ip = "1.2.3.4"
# settings.update()
# print(settings.app_ip)  # Output: '1.2.3.4'

# # Access nested configuration values
# print(settings.mysql.databases.prod)  # Output: 'db1'
# settings.mysql.databases.prod = 'new_value'
# settings.update()
# print(settings.mysql.databases.prod)  # Output: 'new_value'

# # Access and update configuration values
# print(settings.app_ip)  # Output: '1.2.3.4'
# settings.update_config({"app_ip": "1.1.1.1"})
# print(settings.app_ip)  # Output: '1.1.1.1'

# # Access all settings as a dictionary
# all_settings = settings.get_settings()
# print(all_settings)
# # Output: {'app_ip': '1.1.1.1', 'app_host': '', 'app_port': 5000, 'app_upload_folder': 'overridden_uploads', 'mysql_user': 'root', 'mysql_password': 'root', 'mysql_databases': {'prod': 'new_value', 'dev': 'db2'}}

# # Modify values directly in the config dictionary
# settings.config["mysql"]["databases"]["prod"] = "db3"
# settings.update()
# print(settings.mysql_databases["prod"])  # Output: 'db3'

# # Access environment variables
# print(os.environ["PROJECT_MYSQL_DATABASES_PROD"])  # Output: 'db3'
# print(os.environ["PROJECT_APP_UPLOAD_FOLDER"])  # Output: 'overridden_uploads'
