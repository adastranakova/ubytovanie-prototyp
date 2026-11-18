"""Konfigurácia databázy prototypu; heslá patria do lokálneho .env."""
import os
from dotenv import load_dotenv

load_dotenv()


def mysql_settings():
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "swi_demo"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "swi_prototyp"),
        "connection_timeout": 5,
    }
