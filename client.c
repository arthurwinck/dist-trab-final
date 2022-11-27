#include <czmq.h>

int main(int argc, char const *argv[])
{
    // Client -> Requester
    zsock_t *requester = zsock_new(ZMQ_REQ);
    zsock_connect(requester, "tcp://localhost:5555");
    zstr_send(requester, "dale inter");
    sleep(1);
    char *str = zstr_recv(requester);
    printf("%s\n", str);
    zsock_destroy(&requester);
    return 0;
}
