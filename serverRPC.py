from xmlrpc.server import SimpleXMLRPCServer

def add(type, cnpj, id, value):
    return "Operacao: add Type: {type} Cnpj: {cnpj} Id: {id} value: {value}".format(type = type, cnpj = cnpj, id = id, value = value)

def read(type, cnpj, id):
    return "Operacao: read Type: {type} Cnpj: {cnpj} Id: {id}".format(type = type, cnpj = cnpj, id = id)

def remove(type, cnpj, id, value):
    return "Operacao: remove Type: {type} Cnpj: {cnpj} Id: {id} value: {value}".format(type = type, cnpj = cnpj, id = id, value = value)

server = SimpleXMLRPCServer(("localhost", 8888))
server.register_function(add, "add")
server.register_function(read, "read")
server.register_function(remove, "remove")
server.serve_forever()
