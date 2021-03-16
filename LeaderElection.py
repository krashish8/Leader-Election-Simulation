from flask import Flask
from flask import request
from http.client import HTTPConnection
import urllib
import _thread
import get_ip
from random import randint
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

participant = False
leader_PID = 0

my_PID = randint(1, 1000000)

ip = get_ip.get_lan_ip()
print(ip)


headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

pi = int(input("What is my port?: "))
next_pi = int(input("What is the port of the node is next to me?: "))


def send_message(message, path):
    participant = True
    connection = HTTPConnection(ip, next_pi, timeout=10)
    connection.request("POST", ("/" + path), urllib.parse.urlencode({'message' : message}), headers)
    response = connection.getresponse()


def compare(passed):
    global participant
    if (passed > my_PID):
        _thread.start_new_thread(send_PID, (passed, "election"))
    elif (passed < my_PID and  participant == False):
        _thread.start_new_thread(send_PID, (my_PID, "election"))
    elif (passed < my_PID and participant == True):
        print("Discarding election message")
    elif (passed == my_PID):
        participant = False
        _thread.start_new_thread(send_PID, (my_PID, "leader"))




if (input("Start the election? y/n: ")=='y'):
    _thread.start_new_thread(send_PID, (my_PID, "election"))



@app.route('/election', methods=['POST'])
def election():
    passed_PID = int(request.form['PID'])
    _thread.start_new_thread(compare, (passed_PID,))
    return "Starting election"


@app.route('/leader', methods=['POST'])
def leader():
    global participant 
    participant = False
    leader_PID = int(request.form['PID'])
    if (my_PID == leader_PID):
        print("Everyone knows I am the leader now")
        return "I am the leader"
    else:
        print("Leader PID is  " + str(leader_PID))
        _thread.start_new_thread(send_PID, (leader_PID, "leader"))
        return "Leader PID is " + str(leader_PID)




if __name__ == '__main__':
    app.run(port = int(pi), host='0.0.0.0')
