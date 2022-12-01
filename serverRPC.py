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
        listClient = Banco.get_query(con, "cliente", cnpj, qtd)
        if len(listClient) > 0:
            # Tratamento caso exista mais de um cliente com mesmo cnpj, nome (talvez criar unique constraint no banco)
            cliente = listClient[0]
            quantidade = cliente[1] + qtd
            sql = f"""update public.clientes set qtd = {quantidade} where id = {cliente[0]}
            """
        else:
            sql = f"""
                INSERT INTO public.clientes (cnpj, qtd) values ('{cnpj}', {qtd});
            """

        Banco.inserir_db(con, sql)

    def inserir_produto(con, nome, cnpj, qtd):
        listProduct = Banco.get_query(con, "produto", cnpj, nome)
        if len(listProduct) > 0:
            # Tratamento caso exista mais de um cliente com mesmo cnpj, nome (talvez criar unique constraint no banco)
            product = listProduct[0]
            quantidade = product[1] + qtd
            sql = f"""update public.produtos set qtd = {quantidade} where id = {product[0]}
            """
        else:
            sql = f"""
                INSERT INTO public.produtos (cnpj, qtd, nome) values ('{cnpj}', {qtd}, '{nome}');
            """

        Banco.inserir_db(con, sql)

    def remover_produto(con, nome, cnpj, qtd):
        listProduct = Banco.get_query(con, "produto", cnpj, nome)
        if len(listProduct) > 0:
            product = listProduct[0]
            if qtd >= product[1]:
                quantidade = 0
            else:
                quantidade = product[1] - qtd
            sql = f"""update public.produtos set qtd = {quantidade} where id = {product[0]}
            """
            Banco.inserir_db(con, sql)
            return 1

        return 0

    def remover_cliente(con, cnpj, qtd):
        listClient = Banco.get_query(con, "cliente", cnpj, qtd)
        if len(listClient) > 0:
            cliente = listClient[0]
            if qtd >= cliente[1]:
                quantidade = 0
            else:
                quantidade = cliente[1] - qtd

            sql = f"""update public.clientes set qtd = {quantidade} where id = {cliente[0]}
            """
            Banco.inserir_db(con, sql)
            return 1

        return 0

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
            sql = f"""select id, qtd from public.clientes where cnpj = '{cnpj}'
            """

        cur = con.cursor()
        cur.execute(sql)
        recset = cur.fetchall()
        result = []
        for rec in recset:
            result.append(rec)
        cur.close()
        return result


def add(type, cnpj, nome, qtd):
    if type == 'produto':
        Banco.inserir_produto(con_produtos, nome, cnpj, qtd)
        return 'Produtos adicionados'

    else:    
        Banco.inserir_cliente(con_clientes, cnpj, qtd)
        return 'Clientes adicionados'
    
def read(type, cnpj, nome = None):
    connection = type == "produto" and con_produtos or con_clientes
    value = Banco.get_query(connection, type, cnpj, nome)

    return len(value) > 0 and value[0][1] or 0

def remove(type, cnpj, nome, qtd):
    if type == 'produto':
        result = Banco.remover_produto(con_produtos, nome, cnpj, qtd)
    else:
        result = Banco.remover_cliente(con_clientes, cnpj, qtd)

    if result == 1:
        return f'{type} removido'

    return f'sem {type} para remover'


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

# Banco.execute(con_produtos, criar_tab_produtos)
# Banco.execute(con_clientes, criar_tab_clientes)
# Banco.inserir_produto(con_produtos, "pneu", "234578", 1)
# Banco.inserir_cliente(con_clientes, "234578", 100)
# print(Banco.get_query(con_produtos, "produto", "234578", "pneu"))
# print(Banco.get_query(con_clientes, "cliente", "234578"))
# print(Banco.inserir_cliente(con_clientes, "234578", 15))
# print(Banco.get_query(con_clientes, "cliente", "234578"))

print(Banco.get_query(con_produtos, "produto", "234578", "pneu"))
print(Banco.inserir_produto(con_produtos, "pneu", "234578", 15))
print(Banco.get_query(con_produtos, "produto", "234578", "pneu"))


#print(Banco.inserir_cliente(con_clientes, "234578", 15))


# print(Banco.get_produto(con_produtos, 1))
# print(Banco.get_cliente(con_clientes, 1))

# server = SimpleXMLRPCServer(("localhost", 8888))
# server.register_function(add, "add")
# server.register_function(read, "read")
# server.register_function(remove, "remove")
# server.serve_forever()
