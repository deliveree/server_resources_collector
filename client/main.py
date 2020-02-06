import socket
import logging
from psycopg2 import connect

# from client.main import setup

def setup():
    global sock, db_con

    # db_con = connect(
    #     database="",
    #     user="",
    #     password="",
    #     host="localhost",
    # )

server_address = ('18.223.41.243', 15330)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.send(b'BIBIB')
sock.close()



def _get_delay(db):
    query = """SELECT EXTRACT(EPOCH
                FROM (NOW() - pg_last_xact_replay_timestamp()))::INT;"""
    delay = db.query_select(query, fmt="singlevalue") or 0
    return delay


def _get_total_queries_in_queue(db):
    query = """SELECT count(*)
                FROM pg_stat_activity
                WHERE datname = 'deliveree'
                        AND state = 'active'"""
    count = db.query_select(query, fmt="singlevalue") or 0
    return count if count == 0 else count - 1


def _get_load_averages(conn):
    load_average = 0
    load_averages_str = conn.run("uptime | awk -F': ' '{print $2}'")

    if load_averages_str:
        load_average = load_averages_str.stdout.strip().split(', ')[0]

    return load_average


def _get_ram_available(conn):
    ram_available = 0
    ram_available_str = conn.run("free | awk '/Mem:/ {print $3}'")

    if ram_available_str:
        ram_available = ram_available_str.stdout.strip()

    return ram_available


def shutdown():
    db_con.close()
    sock.close()


def main():
    try:
        setup()

        while True:
            delay = _get_delay(db)
            total_queries = _get_total_queries_in_queue(db)
            load_averages = _get_load_averages(conn)
            ram_available = _get_ram_available(conn)

            sock.sendall({
                "delay": delay,
                "total_queries": total_queries,
                "load_averages": load_averages,
                "ram_available": ram_available
            })
    except Exception as ex:
        logging.error(ex)
    finally:
        shutdown()

