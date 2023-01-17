import socket
import threading


class UdpSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message, port, ip_addr="127.0.0.1") -> None:
        self.sock.sendto(message, (ip_addr, port))


class UdpReceiver:
    def __init__(self, port, ip_addr="127.0.0.1", buffer=1024):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port
        self.sock.bind((ip_addr, port))
        self.buffer = buffer

    def receive(self):
        # data_raw, addr = self.sock.recvfrom(self.buffer)
        data_raw = self.sock.recv(self.buffer)
        return data_raw

    def get_port(self):
        return self.sock.getsockname()[1]

    def close(self):
        self.sock.close()


class TcpServer:
    def __init__(self, port, ip_addr="127.0.0.1", buffer=1024):
        self.x = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip_addr = ip_addr
        self._port = port
        self.buffer = buffer
        self.conn = None
        self.waiting_for_con = False
        self._stop = False

    def start(self, callback) -> None:
        self.x = threading.Thread(target=self.receiver_loop, args=(callback,))
        self.x.start()
        while (not self.waiting_for_con):
            pass

    def receiver_loop(self, callback) -> None:
        with self.sock as s:
            s.bind((self._ip_addr, self._port))
            s.listen()
            self.waiting_for_con = True
            self.conn, addr = s.accept()
            with self.conn:
                print(f"Connected by {addr}")
                while (not self._stop):
                    data = self.receive()
                    if not data:
                        break
                    callback(data)

    def stop(self) -> None:
        self._stop = True
        self.x.join()

    def send(self, message) -> None:
        if (self.conn is not None):
            self.conn.sendall(message)

    def receive(self):
        data = self.conn.recv(self.buffer)
        return data


class TcpClient:
    def __init__(self, port, ip_addr="127.0.0.1", buffer=1024):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip_addr = ip_addr
        self._port = port
        self.buffer = buffer
        self.sock.settimeout(5)
        try:
            self.sock.connect((self._ip_addr, self._port))
        except socket.error as msg:
            print("Couldnt connect with the socket-server: %s\n terminating program" % msg)

    def close(self) -> None:
        self.sock.close()
        print("close ", self._ip_addr, " ", self._port)

    def send(self, message) -> None:
        try:
            self.sock.sendall(message)
        except socket.error as msg:
            print("Broken connection, can't send message: %s\n terminating program" % msg)

    def receive(self):
        data = self.sock.recv(self.buffer)
        return data
