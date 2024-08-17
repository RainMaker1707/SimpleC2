#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
from argparse import ArgumentParser
from http.server import HTTPServer
from time import sleep, time
from threading import Thread, Event

import requests
import socket
import random

class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Success</h1></body></html>")
        if self.path[:10] == "/pictures/" and self.path[-4:] == ".png":
            print("Killed")
            stop_event.set()


    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
    

def heartbeat(stop_event, server_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = (30 + random.randint(1, 31)) * 1
    last = 0
    while not stop_event.is_set():
        current = time()
        if current >= last + t or last==0: # simulate sleep but letting the stop_event kill the loop, using sleep doesn't let it happens
            sock.sendto(b'Alive', (server_ip, 5000))
            t = (30 + random.randint(1, 31)) * 1
            print(f'Heartbeat sent. Next heartbeat in {t}s.') 
            last = current
        sleep(.5)

def command_loop(stop_event):
    while not stop_event.is_set():
        match input("$: "):
            case "exit": stop_event.set()
            case _: pass


def run_server(stop_event, ip="0.0.0.0", port=8080, server_class=HTTPServer, handler_class=SimpleHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    # Set a timeout for handle_request to periodically check stop_event
    httpd.timeout = 1  # 1-second timeout
    while not stop_event.is_set():
        httpd.handle_request()  # Handle a single request at a time with a timeout
    httpd.server_close()
    print("HTTP server stopped.\nType ENTER to quit.")


if __name__ == "__main__":
    parser = ArgumentParser(prog="SimpleClient")
    parser.add_argument("ip", type=str)
    args = parser.parse_args()
    print("Server at: ", args.ip)
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

