import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("op,tipo,cnpj,nome (caso seja produto), quantidade (caso seja add ou remove)\n\t"
    "Operações: add, read e remove\n\t"
    "Tipos: \n\t"
    "produtos (quantidade de estoque)\n\t"
    "clientes (quantidade de clientes de um cnpj)\n\t"
    "Exemplo de operacoes:\n\t"
    "Ex: add,cliente,12345,50\n\t"
    "Ex: add,produto,12345,pneu,100\n\t"
    "Ex: read,cliente,12345\n\t"
    "Ex: read,produto,12345,pneu\n\t"
    "Ex: remove,cliente,12345,5\n\t"
    "Ex: remove,produto,12345,pneu,5\n\t")

while True:
    message = input("Send a message\n")
    socket.send_string(message)
    received_message = socket.recv()
    print(received_message.decode())
