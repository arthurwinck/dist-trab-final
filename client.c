#include <czmq.h>
#include <stdio.h>

int main(int argc, char const *argv[])
{
    // Client -> Requester
    zsock_t *requester = zsock_new(ZMQ_REQ);
    zsock_connect(requester, "tcp://localhost:5555");
    char message[100];
    printf("op,tipo,cnpj,nome (caso seja produto), quantidade (caso seja add ou remove)\n\t"
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
    "Ex: remove,produto,12345,pneu,5\n\t");

    while (1) {
        int ret_code = scanf("%[^\n]%*c", message);
        
        if (ret_code == EOF) {
            printf("Terminando o client\n");
            break;
        }

        zstr_send(requester, message);
        char *response = zstr_recv(requester);
        printf("%s\n", response);
    }
    zsock_destroy(&requester);
    return 0;
}
