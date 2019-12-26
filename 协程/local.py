import traceback
import asyncio
import socket
from collections import namedtuple

from asyncio import CancelledError

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

    # asyncio.ensure_future(forward(current_conn, dstIP, dstPort))


local_task_dict = {}
remote_task_dict = {}
gather_task_dict = {}


async def forward(cs, DspAddr, DspPort):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setblocking(False)
    # a = await asyncio.wait_for(loop.sock_connect(ss, (DspAddr, DspPort)), timeout=2)
    try:
        await loop.sock_connect(ss, (DspAddr, DspPort))
        # await asyncio.wait_for(loop.sock_connect(ss, (DspAddr, DspPort)), timeout=2)
    except Exception:
        cs.close()
        ss.close()
        raise

    local_remote = asyncio.ensure_future(local2remote(cs, ss))
    remote_local = asyncio.ensure_future(remote2local(cs, ss))
    local_task_dict[cs] = remote_local
    remote_task_dict[ss] = local_remote
    print("队列长度")
    print(len(local_task_dict))
    print(len(remote_task_dict))
    # gather_task = await asyncio.ensure_future(
    #     asyncio.gather(local_remote, remote_local, loop=loop, return_exceptions=True))


async def local2remote(local_conn, remote_conn):
    while True:
        recv = await loop.sock_recv(local_conn, BUFFER_SIZE)
        if len(recv) > 0:
            await loop.sock_sendall(remote_conn, recv)

        else:
            while True:
                if local_conn in local_task_dict and remote_conn in remote_task_dict:
                    local_conn.close()
                    remote_conn.close()
                    local_task_dict[local_conn].cancel()
                    del local_task_dict[local_conn]
                    del remote_task_dict[remote_conn]
                    # asyncio.current_task().cancel()
                    return
                else:
                    await asyncio.sleep(0.5)


async def remote2local(local_conn, remote_conn):
    while True:
        recv = await loop.sock_recv(remote_conn, BUFFER_SIZE)
        if len(recv) > 0:
            await loop.sock_sendall(local_conn, recv)
        else:
            while True:
                if local_conn in local_task_dict and remote_conn in remote_task_dict:
                    local_conn.close()
                    remote_conn.close()
                    remote_task_dict[remote_conn].cancel()
                    del remote_task_dict[remote_conn]
                    del local_task_dict[local_conn]
                    # asyncio.current_task().cancel()
                    return
                else:
                    await asyncio.sleep(0.5)


async def listen():
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(('0.0.0.0', Port))
    ls.setblocking(False)
    ls.listen(500)
    while True:
        clientSock, address = await loop.sock_accept(ls)
        clientSock.setblocking(False)
        print("0000000000")
        asyncio.ensure_future(prxoy(clientSock, address))


loop = None
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.create_task(listen())
    asyncio.ensure_future(listen())
    loop.run_forever()
