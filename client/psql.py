from psycopg2 import connect, InternalError, InterfaceError
from collections import deque
from socket import getfqdn
import logging


class PSQLConnector():
    def __init__(self, conf, db_type, db_tag):
        hostname = getfqdn()
        self.delay_time = 0
        self.db_config = {
            "database": "",
            "user": "",
            "password": "",
            "host": hostname
        }
        self.conn = self.connect()

    def connect(self):
        db_config = self.db_config
        conn = connect(
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"]
        )

        logging.debug('Successfully connected with ' + self.db_tag)
        return conn

    def execute_select(self, query):
        try:
            cur = conn.cursor()
            cur.execute(query)
            values = cur.fetchall()
            return values[0][0]
        except InternalError as ex:
            logging.error(ex)