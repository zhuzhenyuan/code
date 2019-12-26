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
Port = 7070

BUFFER_SIZE = 1024


async def prxoy(sock, address):
    try:
        # await asyncio.ensure_future(forward(current_conn, dstIP, dstPort))
        loop.create_task(forward(sock, "0.0.0.0", 7071))
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
