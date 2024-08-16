#!/usr/bin/env python3
from argparse import ArgumentParser
from http.server import HTTPServer
from time import sleep, time
from threading import Thread, Event

import requests
import socket
import random

from modules.simple_handler import SimpleHandler
    

def heartbeat(stop_event, server_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = 30 + random.randint(1, 31)
    last = 0
    while not stop_event.is_set():
        if time() < last + t:
            sock.sendto(b'Alive', (server_ip, 5000))
            print("Heartbeat sent.") 
            sleep(t)
            t = 30 + random.randint(1, 31)
            last = time()


def command_loop(stop_event):
    while not stop_event.is_set():
        match input("$: "):
            case "exit": stop_event.set()
            case _: print("Command not recognized")


def run_server(stop_event, ip="0.0.0.0", port=8080, server_class=HTTPServer, handler_class=SimpleHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    # Set a timeout for handle_request to periodically check stop_event
    httpd.timeout = 1  # 1-second timeout
    while not stop_event.is_set():
        httpd.handle_request()  # Handle a single request at a time with a timeout
    httpd.server_close()
    print("HTTP server stopped.")


if __name__ == "__main__":
    parser = ArgumentParser(prog="SimpleClient")
    parser.add_argument("ip", type=str)
    args = parser.parse_args()
    print(args.ip)
    stop_event = Event()
    t1 = Thread(target=heartbeat, args=(stop_event, args.ip, ))
    t2 = Thread(target=command_loop, args=(stop_event, ))
    t3 = Thread(target=run_server, args=(stop_event, ))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

