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
leader_ID = 0

my_ID = randint(1, 1000000)

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
    if (passed > my_ID):
        _thread.start_new_thread(send_message, (passed, "election"))
    elif (passed < my_ID and  participant == False):
        _thread.start_new_thread(send_message, (my_ID, "election"))
    elif (passed < my_ID and participant == True):
        print("Discarding election message")
    elif (passed == my_ID):
        participant = False
        _thread.start_new_thread(send_message, (my_ID, "leader"))




if (input("Start the election? y/n: ")=='y'):
    _thread.start_new_thread(send_message, (my_ID, "election"))



@app.route('/election', methods=['POST'])
def election():
    passed_ID = int(request.form['message'])
    _thread.start_new_thread(compare, (passed_ID,))
    return "Starting election"


@app.route('/leader', methods=['POST'])
def leader():
    global participant 
    participant = False
    leader_ID = int(request.form['message'])
    if (my_ID == leader_ID):
        print("Everyone knows I am the leader now")
        return "I am the leader"
    else:
        print("Leader ID is  " + str(leader_ID))
        _thread.start_new_thread(send_message, (leader_ID, "leader"))
        return "Leader ID is " + str(leader_ID)




if __name__ == '__main__':
    app.run(port = int(pi), host='0.0.0.0')
