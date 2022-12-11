# dist-trab-final
Trabalho final de computação distribuída

[Docs](https://docs.google.com/document/d/1H9ZSVtCMsItGjju_DfFmOGbLV7aRe7U4eROkdcA89wU/edit)

### Rodando a aplicação:

#### Instalar módulos

Docker:
[Como instalar docker no linux](https://www.youtube.com/watch?v=H0RS7bVymw0)

C:
```
sudo apt-get install libczmq-dev
```

Python:
```
pip install -r requirements.txt
```

#### Compilando arquivos em C:

```
gcc client.c -o client -lczmq
```

#### Executando Script para Criar Bancos de dados:

```
./initdb.sh
```

#### Rodando clientes e servidor:

```
./client
```

```
python server.py
```

```
python client.py
```

# Especificação

## Sistema de estoque de produtos já listados 

### Banco de Dados I - produtos (controle de estoque)

Sintaxe de chamada para servidor: 
```
add:read:remove,produto,cnpj,id,quantidade*(add, remove)
```

### Banco de Dados II - clientes (quantidade de clientes)

Sintaxe de chamada para servidor:
```
add:read:delete,cliente,cnpj,quantidade*(add, remove)
```

Operação:

1. Pedir operação para usuário e mandar ela para o servidor:

```
add:read:remove,produto,cnpj,id,quantidade*(add, remove)
```
ou
```
add:read:delete,cliente,cnpj,quantidade*(add, remove)
```

2. Servidor parseia a string e executa chamada de alguma função do RPC (add, read, remove) como parâmetro cliente ou produto  e devolve resultado da operação 

3. RPC faz query ao banco e retorna resultado ao servidor.

4. Cliente recebe resultado do servidor
