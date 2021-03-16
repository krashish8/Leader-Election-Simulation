from flask import Flask
from flask import request
from http.client import HTTPConnection
import urllib
import _thread
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--id', required=True, type=int, help='The ID of the current node')
parser.add_argument('--nodes', required=True, type=int, help = 'Number of nodes in the network')
args = parser.parse_args()

if (args.nodes != 5 and args.nodes != 50 and args.nodes != 100 and args.nodes != 150 and args.nodes != 200):
    print("The number of nodes must be 5, 50, 100, 150 or 200")
    exit(1)

if args.id < 1 or args.id > args.nodes:
    print('The ID of the node must be between 1 and number of nodes')

node_id = args.id
nodes = args.nodes
offset = 8000

node_port = offset + node_id

network = None
with open('data/network-' + str(nodes) + '.json', 'r') as fp:
    network = json.load(fp)

host_ip = '127.0.0.1'

app = Flask(__name__)

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

neighbours_id = network[str(node_id)]["neighbours"]
neighbours_port = list(map(lambda x: x + offset, neighbours_id)) 

import threading
send_message_lock = threading.Lock()

once = 0

def send_message(message, neighbour_port):
    send_message_lock.acquire()
    connection = HTTPConnection(host_ip, neighbour_port)
    connection.request("POST", ("/send"), urllib.parse.urlencode({'id': str(node_id), 'message': message}), headers)
    response = connection.getresponse()
    send_message_lock.release()


send_broadcast_message_lock = threading.Lock()

def send_broadcast_message(message):
    send_broadcast_message_lock.acquire()
    global once
    if once == 1:
        return
    once = 1
    for neighbour_port in neighbours_port:
        send_message(message, neighbour_port)
    send_broadcast_message_lock.release()


mutex = threading.Lock()
event = threading.Event()

def election():
    mutex.acquire()
    # wait for node_id seconds
    if event.wait(node_id):
        # If received any message, then return
        mutex.release()
        return

    # If timeout of node_id seconds occurs
    global once
    if once == 1:
        mutex.release()
        return
    once = 1
    global participant
    # Declare the current node as the leader
    _thread.start_new_thread(send_broadcast_message, (str(node_id)))
    mutex.release()


receive_message_lock = threading.Lock()

@app.route('/send', methods=['POST'])
def receive():
    receive_message_lock.acquire()
    received_from = request.form['id']
    message = request.form['message']

    if (message == "election"):
        # Received an election message
        _thread.start_new_thread(election, ())
    else:
        # Received some other message
        event.set() # Wake the thread calling election() function, and return True there
        _thread.start_new_thread(send_broadcast_message, (message,)) # Broadcast the message to other neighbour nodes
    receive_message_lock.release()
    return 'Received message ' + message


if __name__ == '__main__':
    app.run(port=node_port, host='127.0.0.1')
