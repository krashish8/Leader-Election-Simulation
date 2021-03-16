def send_message(message, neighbour_port):
    participant = True
    connection = HTTPConnection(host_ip, neighbour_port)
    connection.request("POST", ("/send"), urllib.parse.urlencode({'id': node_id, 'message': message}), headers)
    response = connection.getresponse()
