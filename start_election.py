import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--startport', required=True, type=int, help='Starting port of the nodes, to whom the election message is sent')
parser.add_argument('--endport', required=True, type=int, help='Ending port of the nodes, to whom the election message is sent')
args = parser.parse_args()

if (args.startport > args.endport):
    print("Start port must be less than or equal to the end port")
    exit(1)

host_ip = '127.0.0.1'
startport = args.startport
endport = args.endport

def send_message(port):
    connection = HTTPConnection(host_ip, port)
    connection.request("POST", ("/send"), urllib.parse.urlencode({'id': '0', 'message': 'election'}), headers)
    response = connection.getresponse()

import _thread

for port in range(startport, endport + 1):
	_thread.start_new_thread(send_message, (port,))
