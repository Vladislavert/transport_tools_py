import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from typing import Final

from TransportProtocol import UdpReceiver
from TransportProtocol import UdpSender
from ByteBuf import ByteBuf

INT_SIZE: Final[int] = 4
port = 6666
udp_sender = UdpSender()
udp_receiver = UdpReceiver(port)


def udp_send_int_list(array: list[int]) -> None:
    byte_buf = ByteBuf()
    byte_buf.write_int(len(array))
    byte_buf.write_int_list(array)
    udp_sender.send(byte_buf.buffer, port)


def udp_receive_int_list() -> None:
    size = -1
    byte_buf = ByteBuf()
    byte_buf.buffer = udp_receiver.receive()
    if byte_buf.get_size() > INT_SIZE:
        size = byte_buf.read_int()
    if byte_buf.get_size() < size * INT_SIZE:
        print('bad datagram')
        return

    received_list = [byte_buf.read_int() for _ in range(size)]
    print(received_list)


def test() -> None:
    test_data = [1, 2, 3, 4, 5]
    udp_send_int_list(test_data)
    udp_receive_int_list()


if __name__ == "__main__":
    test()
