#!/usr/bin/env python3
from argparse import ArgumentParser
from http.server import HTTPServer
from time import sleep
from threading import Thread, Event

import requests
import socket

from modules.simple_handler import SimpleHandler
    

def heartbeat(stop_event, server_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        sleep(5) 
        sock.sendto(b'Alive', (server_ip, 5000))
        print("Heartbeat sent.") 


def run_server():
    pass


if __name__ == "__main__":
    parser = ArgumentParser(prog="SimpleClient")
    parser.add_argument("ip", type=str)
    args = parser.parse_args()
    print(args.ip)
    stop_event = Event()
    t1 = Thread(target=heartbeat, args=(stop_event, args.ip, ))
    t1.start()

    t1.join()

