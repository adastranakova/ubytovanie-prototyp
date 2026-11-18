"""Jediné miesto vytvárania spojenia s MySQL."""
import mysql.connector
from config import mysql_settings


def spojenie():
    return mysql.connector.connect(**mysql_settings())
