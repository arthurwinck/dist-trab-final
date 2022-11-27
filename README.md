# dist-trab-final
Trabalho final de computação distribuída

### Rodando a aplicação:

#### Instalar módulos do ZeroMQ

C:
`sudo apt-get install libczmq-dev`

Python:
`pip install pyzmq`

#### Compilando arquivos em C:

`gcc client.c -o client -lczmq`

#### Rodando clientes e servidor:

`./client`

`python server.py`

`python client.py`

# Especificação

## Sistema de estoque de produtos já listados 

### Banco de Dados I - produtos (controle de estoque)

Sintaxe de chamada para servidor: 
`/produto/cnpj/add:read:remove/id/quantidade*(add, remove)`

### Banco de Dados II - clientes (quantidade de clientes)

Sintaxe de chamada para servidor:
`/cliente/cnpj/add:read:delete/quantidade*(add, remove)`

Operação:

1. Pedir operação para usuário e mandar ela para o servidor:

`/produto/cnpj/add:read:remove/id/quantidade*(add, remove)`
ou
`/cliente/cnpj/add:read:delete/quantidade*(add, remove)`

2. Servidor parseia a string e executa chamada de alguma função do RPC (add, read, remove) como parâmetro cliente ou produto  e devolve resultado da operação 

3. RPC faz query ao banco e retorna resultado ao servidor.

4. Cliente recebe resultado do servidor
