import select
import traceback
import asyncio
import socket
from collections import namedtuple

Address = namedtuple('Address', 'ip port')
IsNeedAuth = False
Username = 'admin'
Password = '123456'
Port = 7071

BUFFER_SIZE = 1024

sock_list = []
status_dict = {}
comm_dict = {}


def listen():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('0.0.0.0', Port))
    client.setblocking(False)
    client.listen(500)
    sock_list.append(client)
    print(client.fileno())
    while True:
        print(len(sock_list))
        try:
            r_list, w_list, x_list = select.select(sock_list, [], sock_list)
            for r in r_list:
                print("f" + str(r.fileno()))
                print(r.fileno())
                if r is client:
                    clientSock = None
                    try:
                        clientSock, address = client.accept()
                        clientSock.setblocking(False)
                        sock_list.append(clientSock)
                        status_dict[clientSock] = 0
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        if clientSock:
                            clientSock.close()
                else:
                    recv = r.recv(BUFFER_SIZE)
                    buf = bytearray(recv)
                    if r in comm_dict:
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
                    else:
                        if r in status_dict and status_dict[r] == 0:
                            if not buf or buf[0] != 0x05:
                                r.close()
                                sock_list.remove(r)
                                continue

                            r.sendall(bytearray((0x05, 0x00)))
                            status_dict[r] = 1
                        elif r in status_dict and status_dict[r] == 1:
                            ss = None
                            try:
                                current_conn = r
                                print("there is 222222end")
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

                                current_conn.sendall(bytearray((0x05, 0x00, 0x00, 0x01, 0x00, 0x00,
                                                                0x00, 0x00, 0x00, 0x00)))

                                ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                ss.settimeout(3)
                                ss.connect((dstIP, dstPort))
                                ss.setblocking(False)

                                sock_list.append(ss)
                                comm_dict[r] = ss
                                comm_dict[ss] = r
                                if r in status_dict:
                                    del status_dict[r]
                            except Exception as e:
                                print(e)
                                traceback.print_exc()
                                if r:
                                    r.close()
                                if ss:
                                    ss.close()
                                sock_list.remove(r)
                                if r in status_dict:
                                    del status_dict[r]
                                continue
                        else:
                            print("error socket")

            for x in x_list:
                if x in comm_dict:
                    x.close()
                    comm_dict[x].close()
                    sock_list.remove(x)
                    sock_list.remove(comm_dict[x])
                    del comm_dict[comm_dict[x]]
                    del comm_dict[x]
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
