import os
import sys
from time import sleep

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from typing import Final

from TransportProtocol import TcpClient
from TransportProtocol import TcpServer
from ByteBuf import ByteBuf

MSG_SIZE: Final[int] = 5
msg = 'hello'
port = 6666
tcp_server = TcpServer(port)


def callback(data):
    byte_buf = ByteBuf()
    byte_buf.buffer = data
    print(f'received message: {byte_buf.read_string(5)}')


def test() -> None:
    byte_buf = ByteBuf()
    byte_buf.write_string(msg)

    tcp_server.start(callback)
    tcp_client = TcpClient(port)
    tcp_client.send(byte_buf.buffer)

    tcp_client.close()
    tcp_server.stop()


if __name__ == "__main__":
    test()
