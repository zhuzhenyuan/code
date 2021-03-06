import select
import traceback
import asyncio
import socket
from collections import namedtuple

Address = namedtuple('Address', 'ip port')
IsNeedAuth = False
Username = 'admin'
Password = '123456'
Port = 7070

BUFFER_SIZE = 1024

sock_list = []
wait_list = []
status_dict = {}
comm_dict = {}


def listen():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('0.0.0.0', Port))
    client.setblocking(False)
    client.listen(500)
    sock_list.append(client)
    # print(client.fileno())
    while True:
        print("==> " + str(len(sock_list)))
        try:
            r_list, w_list, x_list = select.select(sock_list, wait_list, sock_list + wait_list)
            for r in r_list:
                # print("f" + str(r.fileno()))
                # print(r.fileno())
                if r is client:
                    clientSock = None
                    try:
                        clientSock, address = client.accept()
                        clientSock.setblocking(False)
                        sock_list.append(clientSock)
                        status_dict[clientSock] = 0

                        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        ss.setblocking(False)
                        try:
                            ss.connect(("127.0.0.1", 7071))
                        except BlockingIOError:
                            pass
                        wait_list.append(ss)
                        comm_dict[ss] = clientSock

                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        if clientSock:
                            clientSock.close()
                else:
                    if r in comm_dict:
                        recv = r.recv(BUFFER_SIZE)
                        buf = bytearray(recv)
                        if len(buf) > 0:
                            comm_dict[r].sendall(buf)
                        else:
                            r.close()
                            comm_dict[r].close()
                            sock_list.remove(r)
                            sock_list.remove(comm_dict[r])
                            del comm_dict[comm_dict[r]]
                            del comm_dict[r]
                            if r in status_dict:
                                del status_dict[r]
            for w in w_list:
                wait_list.remove(w)
                comm_dict[comm_dict[w]] = w
                sock_list.append(w)

            for x in x_list:
                x.close()
                comm_dict[x].close()

                if x in sock_list:
                    sock_list.remove(x)
                    sock_list.remove(comm_dict[x])
                    del comm_dict[comm_dict[x]]
                    del comm_dict[x]

                if x in wait_list:
                    wait_list.remove(x)
                    del comm_dict[x]

                if x in comm_dict:
                    if x in status_dict:
                        del status_dict[x]
        except Exception as e:
            print(e)
            traceback.print_exc()
            continue


# loop = None
if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.create_task(listen())
    # asyncio.ensure_future(listen())
    # loop.run_forever()
    listen()
