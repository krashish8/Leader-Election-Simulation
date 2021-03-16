import argparse
from http.client import HTTPConnection
import urllib
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--startport', required=True, type=int, help='Starting port of the nodes, to whom the election message is sent')
parser.add_argument('--endport', required=True, type=int, help='Ending port of the nodes, to whom the election message is sent')
args = parser.parse_args()

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

if (args.startport > args.endport):
    print("Start port must be less than or equal to the end port")
    exit(1)

host_ip = '127.0.0.1'
startport = args.startport
endport = args.endport

def send_message(port):
    connection = HTTPConnection(host_ip, port)
    connection.request("POST", ("/send"), urllib.parse.urlencode({'id': '0', 'message': 'election'}), headers)
    print('Sent message election to ' + str(port))
    response = connection.getresponse()

threads = []

for port in range(startport, endport + 1):
    t1 = threading.Thread(target=send_message, args=(port,)) 
    t1.start()
    threads.append(t1)

for thread in threads:
    thread.join()
