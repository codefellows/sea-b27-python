import threading
import socket

class EchoServer:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print "Socket server starting\n"
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        address = ('127.0.0.1', 50000)
        server_socket.bind(address)
        server_socket.listen(1)
        while self.running:
            connection, client_address = server_socket.accept()
            msg = connection.recv(16)
            connection.sendall(msg)
            connection.shutdown(socket.SHUT_WR)
            connection.close()
        server_socket.close()
        print "Socket server dying\n"

    def stop(self):
        self.running = False


if __name__ == "__main__":
    server = EchoServer()
    server.start()
