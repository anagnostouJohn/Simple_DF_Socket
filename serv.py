#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 13:33:05 2018

@author: john
"""

# Python program to implement server side of chat room.
import socket
import select
import sys
import threading 
import json
from diffiehellman.diffiehellman import DiffieHellman
alice = DiffieHellman()
IP_address = '192.168.168.184'
Port = 8201
def clientthread(conn,addr):
    alice.generate_public_key()
    total_data = ""
    while True:
        try:
            conn.settimeout(1)
            #print("..")
            message = ""
            message = conn.recv(100)
            while message is not "":                
                total_data+=message.decode("utf-8")
                message = "" 
                message = conn.recv(100)
            else:
                break
        except socket.error as ex:
            print(ex)
        x = {"alice":alice.public_key}
        conn.send(json.dumps(x).encode("utf-8"))
        f = json.loads(total_data)
        alice.generate_shared_secret(f["bob"], echo_return_key=True)
        print (alice.shared_key)
        print("END")
        break
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen()
while True :
    try:
        server.settimeout(1)
        conn, addr = server.accept()
        print("EDO")
        t1 = threading.Thread(target = clientthread, args = (conn,addr)) 
        t1.start()
    except socket.error as e:
        print(e)

