import socket
import threading
import select
import time
from collections import namedtuple

Address = namedtuple('Address', 'ip port')
IsNeedAuth = False
Username = 'admin'
Password = '123456'
Port = 7070

BUFFER_SIZE = 1024


def prxoy(sock, address):
    forward(sock, "0.0.0.0", 7071)


def forward(cs, DspAddr, DspPort):
    try:
        # print DspAddr +'\n'
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ss.connect((DspAddr, DspPort))

        cs.setblocking(False)
        ss.setblocking(False)
    except Exception as e:
        print("Connect to ", DspAddr, "Fail")
        return
    socks = []
    socks.append(cs)
    socks.append(ss)
    while (True):
        try:
            r, w, e = select.select(socks, [], [])
            for s in r:
                if s is cs:
                    recv = cs.recv(BUFFER_SIZE)
                    caddr, cport = cs.getpeername()
                    if (len(recv) > 0):
                        saddr, sport = ss.getpeername()
                        print(caddr, ':', cport, '<', len(recv), '>', saddr, ':', sport)
                        ss.send(recv)

                    else:
                        for sock in socks:
                            sock.close()
                        return
                elif s is ss:
                    recv = ss.recv(BUFFER_SIZE)
                    saddr, sport = ss.getpeername()
                    if (len(recv) > 0):
                        caddr, cport = cs.getpeername()
                        print(saddr, ':', sport, '<', len(recv), '>', caddr, ':', cport)
                        cs.send(recv)
                    else:
                        for sock in socks:
                            sock.close()
                        return
        except Exception as e:
            print("Translate data error")
            break


if __name__ == "__main__":
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(('0.0.0.0', Port))
    ls.listen(500)
    while True:
        clientSock, address = ls.accept()
        print("0000000000")
        thread = threading.Thread(target=prxoy, args=(clientSock, address))
        thread.start()
