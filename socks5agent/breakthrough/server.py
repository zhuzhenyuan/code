import select
import threading
import traceback
import asyncio
import socket
from collections import namedtuple

Port = 7001

BUFFER_SIZE = 1024

sock_list = []
s_map = {}


def listen():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('0.0.0.0', Port))
    # client.setblocking(False)
    client.listen(500)
    sock_list.append(client)

    # ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ss.connect(("127.0.0.1", 7000))
    # ss.setblocking(False)

    ss, address = client.accept()
    ss.setblocking(False)
    sock_list.append(ss)
    client.setblocking(False)
    # sock_list.append(ss)
    print("accept it ")

    while True:
        try:
            r_list, w_list, x_list = select.select(sock_list, [], [])
            for sock in r_list:
                if sock == client:
                    try:
                        clientSock, address = sock.accept()
                        clientSock.setblocking(False)
                        sock_list.append(clientSock)
                        s_map[ss] = clientSock
                        print("get one")
                        # s_map[clientSock] = ss
                    except:
                        pass
                elif sock == ss:
                    recv = sock.recv(BUFFER_SIZE)
                    buf = bytearray(recv)
                    if len(buf) > 0:
                        if ss in s_map:
                            s_map[ss].sendall(buf)
                        else:
                            print(recv)
                            ss.send(recv)
                else:
                    recv = sock.recv(BUFFER_SIZE)
                    buf = bytearray(recv)
                    if len(buf) > 0:
                        # s_map[sock].sendall(buf)
                        ss.sendall(buf)
                    else:
                        # sock.close()
                        # s_map[sock].close()
                        sock_list.remove(sock)
                        # sock_list.remove(s_map[sock])
                        # del s_map[s_map[sock]]
                        # del s_map[sock]
                        del s_map[ss]
        # except ConnectionResetError as e:
        #     sock_list.remove(ss)
        #     ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     ss.connect(("127.0.0.1", 7000))
        #     ss.setblocking(False)
        #     sock_list.append(ss)
        #     continue
        except Exception as e:
            print("**")
            print(client)
            print(ss)
            # print(s_map[ss])
            print("**")
            print(e)
            traceback.print_exc()



if __name__ == "__main__":
    a = threading.Thread(target=listen)
    a.start()
    a.join()
