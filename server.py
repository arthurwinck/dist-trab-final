import zmq
import xmlrpc.client

serverRPC = xmlrpc.client.ServerProxy("http://localhost:8888/")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def sendErrorMessage(errorType):
    errorsDict = {
        0 : "Por favor insira a quantidade correta de parametros.",
        1 : "Por favor insira uma operacao valida.",
        2 : "Por favor insira um tipo valido."
    }
    socket.send_string(errorsDict[errorType])

def checkValues(values, operation, type):
    operations = [ "add", "remove", "read" ]
    if not operation in operations:
        sendErrorMessage(1)
        return False

    types = [ "cliente", "produto" ]
    if not type in types:
        sendErrorMessage(2)
        return False

    valuesLen = len(values)

    if ((operation == "add" or operation == "remove") and ((type == "cliente" and valuesLen < 4) or (type == "produto" and valuesLen < 5))):
        sendErrorMessage(0)
        return False
    elif (operation == "read" and ((type == "cliente" and valuesLen < 3) or (type == "produto" and valuesLen < 4))):
        sendErrorMessage(0)
        return False
    else:
        return True

def sendAddOperation(values, type):
    if type == "cliente":
        socket.send_string(serverRPC.add(type, values[2], 0, values[3]))
    else:
        socket.send_string(serverRPC.add(type, values[2], values[3], values[4]))

def sendRemoveOperation(values, type):
    if type == "cliente":
        socket.send_string(serverRPC.remove(type, values[2], 0, values[3]))
    else:
        socket.send_string(serverRPC.remove(type, values[2], values[3], values[4]))

def sendReadOperation(values, type):
    if type == "cliente":
        socket.send_string(serverRPC.remove(type, values[2], 0))
    else:
        socket.send_string(serverRPC.remove(type, values[2], values[3]))

def parseMessage(message):
    values = message.decode().split(",")
    if len(values) < 4:
        sendErrorMessage(0)
        return

    operation = values[0]
    type = values[1]
    if not checkValues(values, operation, type): return

    if operation == "add":
        sendAddOperation(values, type)
    elif operation == "remove":
        sendRemoveOperation(values, type)
    else:
        sendReadOperation(values, type)

while True:
    message = socket.recv()
    parseMessage(message)
