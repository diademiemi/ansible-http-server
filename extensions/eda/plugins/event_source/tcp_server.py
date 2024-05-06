import asyncio
import logging
import time
from typing import Any
import socket
import struct
import os
from multiprocessing import Process, Queue

logger = logging.getLogger(__name__)

async def send_fd(sock, fd):
    """ Send a single file descriptor. """
    sock.sendmsg([b'x'], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('i', fd))])


async def main(queue: asyncio.Queue, args: dict[str, Any]):
    if "port" not in args:
        raise ValueError("Missing required argument: port")
    host = args.get("host", "0.0.0.0")
    port = args["port"]

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Add this line
        server_socket.bind((host, port))
        server_socket.listen(1)

        helper_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        helper_path = "/tmp/ansible_http.sock"
        # try:
        #     helper_sock.connect(helper_path)
        # except socket.error as e:
        #     print(f"Error connecting to helper socket: {e}")
        #     return

        try:
            while True:
                client, addr = server_socket.accept()
                print(f"Accepted connection from {addr}")
                data = client.recv(1024)  # Read some data to trigger FD pass
                if data:
                    await queue.put({"payload": data.decode(), "meta": {"client": addr}})



                    # Wait for /tmp/ansible_http.sock to be created
                    await asyncio.sleep(1)
                    try:
                        helper_sock.connect(helper_path)
                    except socket.error as e:
                        print(f"Error connecting to helper socket: {e}")
                        return


                    await send_fd(helper_sock, client.fileno())
                    break
        finally:
            client.close()
            helper_sock.close()
            server_socket.close()

if __name__ == '__main__':
    asyncio.run(main(asyncio.Queue(), {'port': 8000}))