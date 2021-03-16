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

if (args.nodes != 50 and args.nodes != 100 and args.nodes != 150 and args.nodes != 200):
    print("The number of nodes must be 50, 100, 150 or 200")
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


def send_message(message, neighbour_port):
    participant = True
    connection = HTTPConnection(host_ip, neighbour_port)
    connection.request("POST", ("/send"), urllib.parse.urlencode({'id': node_id, 'message': message}), headers)
    response = connection.getresponse()


def compare(passed):
    global participant
    if (passed > my_ID):
        _thread.start_new_thread(send_message, (passed, "election"))
    elif (passed < my_ID and  participant == False):
        _thread.start_new_thread(send_message, (my_ID, "election"))
    elif (passed < my_ID and participant == True):
        print("Discarding election message")
    elif (passed == my_ID):
        participant = False
        _thread.start_new_thread(send_message, (my_ID, "leader"))


@app.route('/send', methods=['POST'])
def receive():
    received_from = request.form['id']
    message = request.form['message']

    if (message = "election"):
        _thread.start_new_thread(election, (passed_ID,))

    passed_ID = int(request.form['message'])
    return "Starting election"


if __name__ == '__main__':
    app.run(port=port, host='127.0.0.1')
