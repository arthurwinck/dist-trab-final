from xmlrpc.server import SimpleXMLRPCServer
import psycopg2

bd1_db_string = "postgresql://postgres:bd1-distribuida@localhost:5433/bd1-distribuida"
bd2_db_string = "postgresql://postgres:bd1-distribuida@localhost:5434/bd2-distribuida"

def send_message(op, type, cnpj, id, value, success):
    if success:
        return f"Operacao: {op} Type: {type} Cnpj: {cnpj} Id: {id} value: {value}".format(type = type, cnpj = cnpj, id = id, value = value)
    else:
        return f"Operacao Falhou: {op} Type: {type} Cnpj: {cnpj} Id: {id}".format(type = type, cnpj = cnpj, id = id)

class Banco():

    def conecta_db(host, database, user, password, port):
        con = psycopg2.connect(host=host,
                                port=port, 
                                database=database,
                                user=user, 
                                password=password
                                )
        return con

    def execute(con, sql):
        #con = Banco.conecta_db(host, database, user, password)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()

    def inserir_cliente(con, cnpj, qtd):
        # TODO
        # Primeiro dar get no cnpj e id para ver se existe. Se existe, pegar o id e adicionar à quantidade do cliente que já existe
        # Se não, criar um novo cliente com essa quantidade
        hasClient = Banco.get_query(con, "cliente", cnpj, qtd)
        if len(hasClient) > 0:
            quantidade = hasClient[1] + qtd
            sql = f"""update public.clientes set qtd = {quantidade} where id = {hasClient[0]}
            """
        else:
            sql = f"""
                INSERT INTO public.clientes (cnpj, qtd) values ('{cnpj}', {qtd});
            """

        Banco.inserir_db(con, sql)

    def inserir_produto(con, nome, cnpj, qtd):
        # TODO
        # Primeiro dar get no nome e cnpj e id para ver se existe. Se existe, pegar o id e adicionar à quantidade do produto que já existe
        # Se não, criar um novo produto com essa quantidade
        hasProduct = Banco.get_query(con, "produto", cnpj, qtd)
        if len(hasProduct) > 0:
            quantidade = hasProduct[1] + qtd
            sql = f"""update public.produtos set qtd = {quantidade} where id = {hasProduct[0]}
            """
        else:
            sql = f"""
                INSERT INTO public.produto (cnpj, qtd, nome) values ('{cnpj}', {qtd}, '{nome}');
            """

        Banco.inserir_db(con, sql)

    def inserir_db(con, sql):
        #con = Banco.conecta_db()
        cur = con.cursor()
        try:
            cur.execute(sql)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            con.rollback()
            cur.close()
            return 1
        cur.close()

    def get_query(con, type, cnpj, nome = None):
        if type == "produto":
            sql = f"""select id, qtd from public.produtos where cnpj = '{cnpj}' and nome = '{nome}'
            """
        else:
            sql = f"""select id, qtd from public.produtos where cnpj = '{cnpj}'
            """

        cur = con.cursor()
        cur.execute(sql)
        recset = cur.fetchall()
        result = []
        for rec in recset:
            result.append(rec)
        cur.close()
        return result


def add(type, cnpj, id, value):
    if type == 'produto':
        Banco.inserir_produto(con_produtos, "pasta de dente", "234578", 5)
        return send_message(type, cnpj, id, value, 1)
    
    elif type == 'cliente':    
        Banco.inserir_cliente(con_clientes, "234578", 16)
        return send_message(type, cnpj, id, value, 1)
    else:
        return send_message(type, cnpj, id, value, 0)
    
def read(type, cnpj, id):
    value = Banco.get_query(con_produtos, type, 'cnpj', cnpj)

    if len(value) > 0:
        return send_message(type, cnpj, id, value, 1)
    else:
        return send_message(type, cnpj, id, value, 0)


def remove(type, cnpj, id):
    send_message(type, cnpj, id, value, 1)


con_produtos = Banco.conecta_db('localhost', 'bd1-distribuida', 'postgres', 'bd1-distribuida', 5433)
con_clientes = Banco.conecta_db('localhost', 'bd2-distribuida', 'postgres', 'bd2-distribuida', 5434)

criar_tab_produtos = """
    CREATE TABLE public.produtos
    (
        id integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
        cnpj character varying(20),
        nome character varying(100),
        qtd int NOT NULL
    );
"""
criar_tab_clientes = """
    CREATE TABLE public.clientes
    (
        id integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
        cnpj character varying(20),
        qtd int NOT NULL
    );

"""

Banco.execute(con_produtos, criar_tab_produtos)
Banco.execute(con_clientes, criar_tab_clientes)
Banco.inserir_produto(con_produtos, "pneu", "234578", 1)
Banco.inserir_cliente(con_clientes, "234578", 16)

print(Banco.get_produto(con_produtos, 1))
print(Banco.get_cliente(con_clientes, 1))

server = SimpleXMLRPCServer(("localhost", 8888))
server.register_function(add, "add")
server.register_function(read, "read")
server.register_function(remove, "remove")
server.serve_forever()
