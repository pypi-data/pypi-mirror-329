import os
import sys

from square_authentication_helper import SquareAuthenticationHelper
from square_commons import ConfigReader
from square_database_helper import SquareDatabaseHelper, FiltersV0
from square_database_helper.pydantic_models import FilterConditionsV0
from square_database_structure.square import global_string_database_name
from square_database_structure.square.public import global_string_schema_name
from square_database_structure.square.public.tables import App
from square_logger.main import SquareLogger

try:
    config_file_path = (
        os.path.dirname(os.path.abspath(__file__))
        + os.sep
        + "data"
        + os.sep
        + "config.ini"
    )
    ldict_configuration = ConfigReader(config_file_path).read_configuration()

    # get all vars and typecast
    # ===========================================
    # general
    config_str_module_name = ldict_configuration["GENERAL"]["MODULE_NAME"]
    config_str_app_name = ldict_configuration["GENERAL"]["APP_NAME"]
    # ===========================================

    # ===========================================
    # environment
    config_str_host_ip = ldict_configuration["ENVIRONMENT"]["HOST_IP"]
    config_int_host_port = int(ldict_configuration["ENVIRONMENT"]["HOST_PORT"])
    config_str_log_file_name = ldict_configuration["ENVIRONMENT"]["LOG_FILE_NAME"]
    config_str_admin_password_hash = ldict_configuration["ENVIRONMENT"][
        "ADMIN_PASSWORD_HASH"
    ]

    config_str_ssl_crt_file_path = ldict_configuration["ENVIRONMENT"][
        "SSL_CRT_FILE_PATH"
    ]
    config_str_ssl_key_file_path = ldict_configuration["ENVIRONMENT"][
        "SSL_KEY_FILE_PATH"
    ]
    config_str_cookie_domain = ldict_configuration["ENVIRONMENT"]["COOKIE_DOMAIN"]
    # ===========================================

    # ===========================================
    # square_logger
    config_int_log_level = int(ldict_configuration["SQUARE_LOGGER"]["LOG_LEVEL"])
    config_str_log_path = ldict_configuration["SQUARE_LOGGER"]["LOG_PATH"]
    config_int_log_backup_count = int(
        ldict_configuration["SQUARE_LOGGER"]["LOG_BACKUP_COUNT"]
    )
    # ===========================================

    # ===========================================
    # square_database_helper

    config_str_square_database_protocol = ldict_configuration["SQUARE_DATABASE_HELPER"][
        "SQUARE_DATABASE_PROTOCOL"
    ]
    config_str_square_database_ip = ldict_configuration["SQUARE_DATABASE_HELPER"][
        "SQUARE_DATABASE_IP"
    ]
    config_int_square_database_port = int(
        ldict_configuration["SQUARE_DATABASE_HELPER"]["SQUARE_DATABASE_PORT"]
    )
    # ===========================================
    # ===========================================
    # square_authentication_helper

    config_str_square_authentication_protocol = ldict_configuration[
        "SQUARE_AUTHENTICATION_HELPER"
    ]["SQUARE_AUTHENTICATION_PROTOCOL"]
    config_str_square_authentication_ip = ldict_configuration[
        "SQUARE_AUTHENTICATION_HELPER"
    ]["SQUARE_AUTHENTICATION_IP"]
    config_int_square_authentication_port = int(
        ldict_configuration["SQUARE_AUTHENTICATION_HELPER"][
            "SQUARE_AUTHENTICATION_PORT"
        ]
    )
    # ===========================================
    # Initialize logger
    global_object_square_logger = SquareLogger(
        pstr_log_file_name=config_str_log_file_name,
        pint_log_level=config_int_log_level,
        pstr_log_path=config_str_log_path,
        pint_log_backup_count=config_int_log_backup_count,
    )

    global_object_square_database_helper = SquareDatabaseHelper(
        param_str_square_database_ip=config_str_square_database_ip,
        param_int_square_database_port=config_int_square_database_port,
        param_str_square_database_protocol=config_str_square_database_protocol,
    )
    global_object_square_authentication_helper = SquareAuthenticationHelper(
        param_str_square_authentication_protocol=config_str_square_authentication_protocol,
        param_str_square_authentication_ip=config_str_square_authentication_ip,
        param_int_square_authentication_port=config_int_square_authentication_port,
    )
    # get app id
    global_int_app_id = global_object_square_database_helper.get_rows_v0(
        database_name=global_string_database_name,
        schema_name=global_string_schema_name,
        table_name=App.__tablename__,
        filters=FiltersV0(
            root={
                App.app_name.name: FilterConditionsV0(eq=config_str_app_name),
            }
        ),
        columns=[App.app_id.name],
    )["data"]["main"][0][App.app_id.name]
except Exception as e:
    print(
        "\033[91mMissing or incorrect config.ini file.\n"
        "Error details: " + str(e) + "\033[0m"
    )
    sys.exit()
