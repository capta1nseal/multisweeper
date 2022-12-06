import socket
from _thread import *
import sys

HOST = "localhost"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST,PORT))
server.listen(2)  # max clients

print("Server started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = server.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
