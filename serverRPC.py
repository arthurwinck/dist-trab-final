from xmlrpc.server import SimpleXMLRPCServer
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

bd1_db_string = "postgresql://postgres:bd1-distribuida@localhost:5433/bd1-distribuida"
bd2_db_string = "postgresql://postgres:bd1-distribuida@localhost:5434/bd2-distribuida"

db_produtos = create_engine(bd1_db_string)
db_clientes = create_engine(bd2_db_string)

baseProdutos = declarative_base()
baseClientes = declarative_base()


class Produtos(baseProdutos):
    __tablename__ = 'produtos'
    id = Column('id', Integer, Sequence("id_produtos", start=1), primary_key=True),
    cnpj = Column('cnpj', String(length=14)),
    nome = Column('nome', String(collation='utf-8', length=100)),
    quantidade = Column('quantidade', Integer)
    

class Clientes(baseClientes):
    id = Column('id', Integer, Sequence("id_clientes", start=1), primary_key=True),
    cnpj = Column('cnpj', String(length=14)),
    quantidade = Column('quantidade', Integer)
    
baseClientes.metadata.create_all(db_clientes)
baseProdutos.metadata.create_all(db_produtos)


SessionProduto = sessionmaker(db_produtos)
produtos_session = SessionProduto()

SessionClientes = sessionmaker(db_clientes)
clientes_session = SessionClientes()


def create_tables(db_produtos, db_clientes):
    

    # meta = MetaData(db_produtos)
    # tabela_produtos = Table('produtos', meta,
    #     Column('id', Integer, Sequence("id_produtos", start=1), primary_key=True),
    #     Column('cnpj', String(length=14)),
    #     Column('nome', String(collation='utf-8', length=100)),
    #     Column('quantidade', Integer)
    # )

    produtos_session.add(tabela_produtos)
    produtos_session.commit()



    # tabela_clientes = Table('clientes', meta,
    #     Column('id', Integer, Sequence("id_clientes", start=1), primary_key=True),
    #     Column('cnpj', String(length=14)),
    #     Column('quantidade', Integer)
    # )

    clientes_session.add(tabela_clientes)
    clientes_session.commit()


def add(type, cnpj, id, value):
    return "Operacao: add Type: {type} Cnpj: {cnpj} Id: {id} value: {value}".format(type = type, cnpj = cnpj, id = id, value = value)

def read(type, cnpj, id):
    return "Operacao: read Type: {type} Cnpj: {cnpj} Id: {id}".format(type = type, cnpj = cnpj, id = id)

def remove(type, cnpj, id, value):
    return "Operacao: remove Type: {type} Cnpj: {cnpj} Id: {id} value: {value}".format(type = type, cnpj = cnpj, id = id, value = value)


#create_tables(db_produtos, db_clientes)

# server = SimpleXMLRPCServer(("localhost", 8888))
# server.register_function(add, "add")
# server.register_function(read, "read")
# server.register_function(remove, "remove")
# server.serve_forever()
