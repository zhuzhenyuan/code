import socket
import threading
import select
import time
from collections import namedtuple

Address = namedtuple('Address', 'ip port')
IsNeedAuth = False
Username = 'admin'
Password = '123456'
Port = 7071

BUFFER_SIZE = 1024


def prxoy(sock, address):
    print(address)

    current_conn = sock
    DspPort = 0
    DspAddr = ''
    try:
        buf = current_conn.recv(BUFFER_SIZE)
        buf = bytearray(buf)
        if not buf or buf[0] != 0x05:
            current_conn.close()
            return

        current_conn.sendall(bytearray((0x05, 0x00)))

        buf = current_conn.recv(BUFFER_SIZE)
        buf = bytearray(buf)
        if len(buf) < 7:
            current_conn.close()
            return

        if buf[1] != 0x01:
            current_conn.close()
            return

        dstIP = None

        dstPort = buf[-2:]
        dstPort = int(dstPort.hex(), 16)

        dstFamily = None

        if buf[3] == 0x01:
            # ipv4
            dstIP = socket.inet_ntop(socket.AF_INET, buf[4:4 + 4])
            dstAddress = Address(ip=dstIP, port=dstPort)
            dstFamily = socket.AF_INET
        elif buf[3] == 0x03:
            # domain
            dstIP = buf[5:-2].decode()
            dstAddress = Address(ip=dstIP, port=dstPort)
        elif buf[3] == 0x04:
            # ipv6
            dstIP = socket.inet_ntop(socket.AF_INET6, buf[4:4 + 16])
            dstAddress = (dstIP, dstPort, 0, 0)
            dstFamily = socket.AF_INET6
        else:
            current_conn.close()
            return

        # dstServer = None
        # if dstFamily:
        #     try:
        #         dstServer = socket.socket(
        #             family=dstFamily, type=socket.SOCK_STREAM)
        #         dstServer.setblocking(False)
        #         await self.loop.sock_connect(dstServer, dstAddress)
        #     except OSError:
        #         if dstServer is not None:
        #             dstServer.close()
        #             dstServer = None
        # else:
        #     host, port = dstAddress
        #     for res in socket.getaddrinfo(host, port):
        #         dstFamily, socktype, proto, _, dstAddress = res
        #         try:
        #             dstServer = socket.socket(dstFamily, socktype, proto)
        #             dstServer.setblocking(False)
        #             await self.loop.sock_connect(dstServer, dstAddress)
        #             break
        #         except OSError:
        #             if dstServer is not None:
        #                 dstServer.close()
        #                 dstServer = None
        #
        # if dstFamily is None:
        #     current_conn.close()
        #     return

        current_conn.sendall(bytearray((0x05, 0x00, 0x00, 0x01, 0x00, 0x00,
                                        0x00, 0x00, 0x00, 0x00)))

        forward(current_conn, dstIP, dstPort)
        # forward(current_conn, DspAddr, DspPort)
    except Exception as e:
        print(e)


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
