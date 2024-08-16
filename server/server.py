#!/usr/bin/env python3
from http.server import HTTPServer
from threading import Thread, Event

import sys
import requests
import random
import socket

from modules.simple_handler import SimpleHandler
from dictionnaries.file_name import files
from dictionnaries.task_name import tasks


def help():
    print("Here is the help. You'll don't have real help as it is a fictional framework")


def send(req):
    return



def build_uri_task(ext='.js'):
    uri_start = '/scripts/'
    return


def build_uri_file(uri_start='/pictures/', ext='.png'):
    return uri_start + random.choice(files) + ext


def run_server(stop_event, ip="0.0.0.0", port=8080, server_class=HTTPServer, handler_class=SimpleHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    # Set a timeout for handle_request to periodically check stop_event
    httpd.timeout = 1  # 1-second timeout
    while not stop_event.is_set():
        httpd.handle_request()  # Handle a single request at a time with a timeout
    httpd.server_close()
    print("HTTP server stopped.")


def command_loop(stop_event):
    while not stop_event.is_set():
        user_in = input("$: ")
        match user_in:
            case "help": help()
            case "screen": pass # will use order model
            case "ls": pass # will use tasking model
            case "kill": pass # will kill the distant process

            case "exit": 
                stop_event.set()
            case _: print("Command not recognized")


def receive_heartbeat(stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5000))
    while not stop_event.is_set():
        data, addr = sock.recvfrom(512)
        print(f'received {data} from {addr}')



if __name__ == "__main__":
    print("ok")
    print(build_uri_file())

    stop_event = Event()


    t1 = Thread(target=run_server, args=(stop_event, ))
    print("HTTP server listening.")
    t2 = Thread(target=command_loop, args=(stop_event, ))
    t3 = Thread(target=receive_heartbeat, args=(stop_event, ))
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()