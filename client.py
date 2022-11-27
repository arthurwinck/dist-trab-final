import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    message = input("Send a message\n")
    socket.send_string(message)
    received_message = socket.recv()
    print(received_message.decode())
