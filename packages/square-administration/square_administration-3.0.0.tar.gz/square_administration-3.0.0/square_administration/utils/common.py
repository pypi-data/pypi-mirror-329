import os

from square_administration.configuration import (
    config_str_ssl_key_file_path,
    config_str_ssl_crt_file_path,
)


def is_https() -> bool:
    return os.path.exists(config_str_ssl_key_file_path) and os.path.exists(
        config_str_ssl_crt_file_path
    )
