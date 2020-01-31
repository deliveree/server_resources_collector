from redis import Redis


class RedisConnector():
    def __init__(self):
        self.conn = Redis(host="localhost", db=4)