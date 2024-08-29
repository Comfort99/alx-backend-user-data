#!/usr/bin/env python3
""" Logging Model """
import logging
from mysql.connector.connection import MySQLConnection
from os import environ
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns an Obfuscate PII Fields """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """ A logging Instatiator """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(streamHandler)

    return logger


def get_db() -> MySQLConnection:
    """ Return a connector to MySQL database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    passwrd = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    try:
        connection = mysql.connector.connect(usr=username,
                                             password=passwrd,
                                             host=host,
                                             database=db_name)
    except mysql.connection.Error as error:
        print(error)
    return connection


def main():
    """  Obtain a database connection using get_db and retrieves all rows
        in the users table and display each row under a filtered format """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    field_names = [i[0] for i in cursor.description]
    logger = get_logger()

    for row in cursor:
        strRow = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(strRow.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
