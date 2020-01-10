import select
import threading
import traceback
import asyncio
import socket
from collections import namedtuple

# Port = 7001

BUFFER_SIZE = 1024

sock_list = []
s_map = {}


def listen():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(("127.0.0.1", 7001))
    client.connect(("47.102.125.88", 7001))
    client.setblocking(False)
    # client.listen(500)
    sock_list.append(client)

    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect(("127.0.0.1", 7000))
    # ss.connect(("127.0.0.1", 22))
    ss.setblocking(False)
    sock_list.append(ss)

    while True:
        try:
            r_list, w_list, x_list = select.select(sock_list, [], [])
            for sock in r_list:
                if sock == client:
                    recv = sock.recv(BUFFER_SIZE)
                    buf = bytearray(recv)
                    if len(buf) > 0:
                        ss.sendall(buf)
                elif sock == ss:
                    recv = sock.recv(BUFFER_SIZE)
                    buf = bytearray(recv)
                    if len(buf) > 0:
                        client.sendall(buf)
                # else:
                #     recv = sock.recv(BUFFER_SIZE)
                #     buf = bytearray(recv)
                #     if len(buf) > 0:
                #         # s_map[sock].sendall(buf)
                #         ss.sendall(buf)
                #     else:
                #         # sock.close()
                #         # s_map[sock].close()
                #         sock_list.remove(sock)
                #         # sock_list.remove(s_map[sock])
                #         # del s_map[s_map[sock]]
                #         # del s_map[sock]
        except ConnectionResetError as e:
            print(e)
            sock_list.remove(ss)
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.connect(("127.0.0.1", 7000))
            ss.setblocking(False)
            sock_list.append(ss)
            continue
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
