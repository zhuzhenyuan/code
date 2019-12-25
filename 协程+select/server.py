import asyncio
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


async def prxoy(sock, address):
    print(address)

    current_conn = sock
    DspPort = 0
    DspAddr = ''
    try:
        buf = await loop.sock_recv(current_conn, BUFFER_SIZE)
        buf = bytearray(buf)
        if not buf or buf[0] != 0x05:
            current_conn.close()
            return

        await loop.sock_sendall(current_conn, bytearray((0x05, 0x00)))

        buf = await loop.sock_recv(current_conn, BUFFER_SIZE)
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

        await loop.sock_sendall(current_conn, bytearray((0x05, 0x00, 0x00, 0x01, 0x00, 0x00,
                                                         0x00, 0x00, 0x00, 0x00)))

        # await asyncio.ensure_future(forward(current_conn, dstIP, dstPort))
        loop.create_task(forward(current_conn, dstIP, dstPort))
        print("***********")
        print("***********")
        print(asyncio.all_tasks())
        print(len(asyncio.all_tasks()))
        print("***********")
        print("***********")
    except Exception as e:
        print(e)


async def forward(cs, DspAddr, DspPort):
    print("ggggggggggggggggggg")
    try:
        # print DspAddr +'\n'
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # cs.setblocking(False)
        ss.setblocking(False)
        # await loop.sock_connect(ss, (DspAddr, DspPort))
        await loop.sock_connect(ss, (DspAddr, DspPort))

        # ss.connect()


    except Exception as e:
        print("Connect to ", DspAddr, "Fail")
        return
    socks = []
    socks.append(cs)
    socks.append(ss)
    while (True):
        try:
            # print("22222")
            r, w, e = select.select(socks, [], [], 0)  # timeout设置为0，表示不阻塞
            # print(r)
            # print(w)
            # print(e)
            if not r:  # 释放cpu占用
                await asyncio.sleep(0)
            for s in r:
                # print("11111")
                if s is cs:
                    # print("cscscscscscscscs")
                    recv = await loop.sock_recv(cs, BUFFER_SIZE)
                    # recv = cs.recv(BUFFER_SIZE)
                    caddr, cport = cs.getpeername()
                    if (len(recv) > 0):
                        saddr, sport = ss.getpeername()
                        # print(caddr, ':', cport, '<', len(recv), '>', saddr, ':', sport)
                        # ss.send(recv)
                        await loop.sock_sendall(ss, recv)
                        # ss.sendall(recv)

                    else:
                        for sock in socks:
                            sock.close()
                        return
                        # cs.close()
                        # break
                elif s is ss:
                    # print("sssssssssss")
                    recv = await loop.sock_recv(ss, BUFFER_SIZE)
                    # recv = ss.recv(BUFFER_SIZE)
                    saddr, sport = ss.getpeername()
                    if (len(recv) > 0):
                        caddr, cport = cs.getpeername()
                        # print("ssss11111111")
                        # print(saddr, ':', sport, '<', len(recv), '>', caddr, ':', cport)
                        # cs.send(recv)
                        await loop.sock_sendall(cs, recv)
                        # print("sssss22222222")
                        # cs.sendall(recv)
                    else:
                        for sock in socks:
                            sock.close()
                        return
                        # ss.close()
                        # break
                # print("ddddddddddddd")
        except Exception as e:
            print(e)
            print("Translate data error")
            break


async def listen():
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(('0.0.0.0', Port))
    ls.setblocking(False)
    ls.listen(500)
    ls.setblocking(False)
    while True:
        clientSock, address = await loop.sock_accept(ls)
        clientSock.setblocking(False)
        print("0000000000")
        # asyncio.ensure_future(prxoy(clientSock, address))
        loop.create_task(prxoy(clientSock, address))



loop = None
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.create_task(listen())
    asyncio.ensure_future(listen())
    # asyncio.run(listen())
    loop.run_forever()
