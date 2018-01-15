import json
import socket
import sys
import importlib
from pd_utility import matcher
from thread import *

"""
PYTHON-DANCE v0.1
SERVER'S CORE. PLS DO NOT TOUCH UNLESS YOU ARE SURE OF WHAT YOU ARE DOING.
"""

NL = "\r\n"

print ("Python Dance v0.1")
print ("Initializing...")

init = json.load(open("init.json"))                         # Loading and parsing the init.json file in the root folder.
i = importlib.import_module(init["module"])                 # import the specified module in the init.json file.

# Call the on_load function.
if 'on_load' in init:
    if hasattr(i, init["on_load"]):
        on_load = getattr(i, init["on_load"])
        on_load()
    else:
        print ("Warning, on_load function not found.")

print ("Initialized.")
print ("Creating Socket...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create the socket object.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # Make address re-usable.

print ("Binding Socket to Port {}...".format(init["port"]))

try:
    s.bind((init["host"], init["port"]))                     # Bind to given host and port
except socket.error, msg:
    print ("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
    sys.exit()

print ("Socket Successfully Bound to Port {}.".format(init["port"]))

s.listen(10)

print ("Socket is Listening...")


def client_thread(connection, ip, port):
    """
    function for taking in and processing an incoming connection from a client. not that this function is called and
    forked off the main thread to allow multiple clients communicate simultaneously.
    :param connection: socket object
    :param ip: ip address of the client
    :param port: the port number the client originated the connection from.
    :return: None
    """
    buff = ""
    used = False
    append_buffer = False
    keep_alive = False
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
                    func = getattr(i, rule["match_call"])
                    response = func(payload)
                    if isinstance(response, dict):
                        response = json.dumps(response)
                        print ("Sending Back -> {}.".format(response))
                        connection.sendall(response + NL)
                    if 'keep_alive' in rule:
                        if rule["keep_alive"] != 1:
                            connection.close()
                    elif not keep_alive:
                        connection.close()
                        print ("Closed Connection with {}:{}".format(ip, port))
                        sys.exit()
                    break


while True:
    conn, address = s.accept()

    print 'Connected with ' + address[0] + ':' + str(address[1])

    start_new_thread(client_thread, (conn, address[0], address[1],))

print("Shutdown Signal Received.")
