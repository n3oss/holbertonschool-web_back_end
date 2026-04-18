#!/usr/bin/env python3
"""
Module for handling personal data securely.
"""

import logging
import os
import re
from typing import List
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Return the log message with specified fields obfuscated.
    """
    for field in fields:
        pattern = f"{field}=[^{separator}]*"
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Formatter that redacts specified fields in log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Return the formatted log record with sensitive fields redacted.
        """
        original_log = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Return a logger configured to redact PII fields.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


def get_db() -> "mysql.connector.connection.MySQLConnection":
    """
    Return a connection to the MySQL database.
    """
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """
    Retrieve all rows in the users table and display them with PII redacted.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    headers = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        message = "; ".join(f"{h}={v}" for h, v in zip(headers, row)) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
