from psycopg2 import connect, InternalError, InterfaceError
from collections import deque
from socket import getfqdn
import ../credentials.py as cred
import logging


class PSQLConnector():
    def __init__(self, conf, db_type, db_tag):
        hostname = getfqdn()

        self.delay_time = 0
        self.db_config = {
            "database": cred.database,
            "user": cred.user,
            "password": cred.password,
            "host": hostname
        }
        self.conn = self.connect()

    def connect(self):
        db_config = self.db_config
        conn = connect(
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host="localhost"
        )

        logging.debug('Successfully connected with ' + db_config["host"])
        return conn

    def execute_select(self, query):
        try:
            cur = conn.cursor()
            cur.execute(query)
            values = cur.fetchall()
            return values[0][0]
        except InternalError as ex:
            logging.error(ex)