import unittest
import Redis


def send_figures_to_server():
    con = Redis(host="localhost", db=4)
    prefix = "resources_collector"
    host = "localhost"

    for key in ("delay", "total_queries", "load_averages", "ram_available"):
        assertIsNotNone(con.get(":".join((prefix, host, key))))
