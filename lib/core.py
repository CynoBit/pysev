import json
import socket
import sys

print ("Python Dance v0.1")
print ("Initializing...")
print ("Loading Configurations")

init = json.load(open("init.json"))

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