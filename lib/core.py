import json
import socket
import sys
import importlib
from pd_utility import matcher
from thread import *

print ("Python Dance v0.1")
print ("Initializing...")
print ("Loading Configurations")

init = json.load(open("init.json"))
i = importlib.import_module(init["module"])

print ("Configurations Loaded")
print ("Creating Socket...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print ("Socket Created.")
print ("Binding Socket to Port {}...".format(init["port"]))

try:
    s.bind((init["host"], init["port"]))
except socket.error, msg:
    print ("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
    sys.exit()

print ("Socket Bound to Port {}.".format(init["port"]))

s.listen(10)

print ("Socket is Listening...")


def client_thread(connection, ip, port):
    buff = ""
    used = False
    append_buffer = False
    while True:
        data = connection.recv(1024)
        print ("Received Data: " + data.strip())
        try:
            if append_buffer:
                read_buffer = buff + data.strip()
            else:
                read_buffer = data.strip()
            payload = json.loads(read_buffer)
            buff = ""
        except ValueError:
            payload = None
            if not data:
                try:
                    payload = json.loads(buff)
                    buff = ''
                except ValueError:
                    if used:
                        print("Connection Closed")
                        sys.exit()
                    else:
                        print("Unknown Protocol")
                        print('Closing connection with ' + str(ip) + ":" + str(port))
                        sys.exit()
            else:
                print("Incoming Data Buffered")
                buff += data.strip()
                append_buffer = True
            print(buff)
        if not payload:
            if len(buff) > 0:
                continue
            if len(data) > 0:
                print("Unknown Protocol")
            else:
                print 'Error Receiving Data'
            print 'Closing connection with ' + str(ip) + ":" + str(port)
            break
        else:
            for rule in init["rules"]:
                if matcher.is_match(rule["conditions"], payload):
                    func = getattr(i, rule["call"])
                    connection.sendall(func(payload))
                    connection.close()
                    print ("Connection Closed")
                    sys.exit()


while True:
    conn, address = s.accept()
    # display client information
    print 'Connected with ' + address[0] + ':' + str(address[1])
    start_new_thread(client_thread, (conn, address[0], address[1],))

print("Shutdown Signal Received.")
