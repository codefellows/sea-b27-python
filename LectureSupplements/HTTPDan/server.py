"""
HTTPDan is a basic web server similar to httpd but better (maybe).
"""
import socket
from threading import Thread
import Queue
import time


class SocketServer(Thread):
    """
    The SocketServer encapsulates a low level socket option with the logic required to
    bind and listen for incoming TCP connections. To prevent slowing down the server from
    handling new connections, each accepted connection is queued up for a worker thread
    to implement the protocol with.
    """
    def __init__(self, conn_queue, ip="127.0.0.1", port=8888):
        Thread.__init__(self, name="SocketServerThread")
        self.conn_queue = conn_queue
        self.ip = ip
        self.port = port
        self.running = False

    def start(self):
        self.running = True
        Thread.start(self)

    def run(self):
        print "[SocketServer] starting server run loop"
        address = (self.ip, self.port)
        httpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        httpSock.bind(address)
        httpSock.listen(1)
        while self.running:
            print "[SocketServer] waiting to accept new connection"
            self.conn_queue.put(httpSock.accept())
        print "[SocketServer] shutting down socket server"
        httpSock.shutdown()
        httpSock.close()

    def stop():
        self.running = False


class ProtocolWorker(Thread):
    """
    The ProtocolWorker encapsulates how to handle open connections from the connection
    queue. It does this by pulling messages in a non-blocking way from the connection
    queue and then executing the protocol logic. To implement specific protocol logic,
    you should extend this class and overwrite the execute_protocol_logic method to do
    your specific task.
    """
    def __init__(self, conn_queue):
        Thread.__init__(self, name="WorkerThread")
        self.conn_queue = conn_queue
        self.running = False

    def execute_protocol_logic(self, conn, client_addr):
        pass

    def start(self):
        self.running = True
        Thread.start(self)

    def stop(self):
        self.running = False

    def run(self):
        print "[ProtocolWorker] scanning connection queue for new work"
        while self.running:
            conn = None
            try:
                conn, client_addr = self.conn_queue.get_nowait()
                self.execute_protocol_logic(conn, client_addr)
            except Queue.Empty:
                time.sleep(1) # attempt to not thrash
            except Exception as ex:
                print "[ProtocolWorker] got an exception - %s" % (ex,)
            finally:
                if conn is not None:
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()


class HttpProtocolWorker(ProtocolWorker):
    """
    Implements HTTP, Dan style
    """
    def __init__(self, conn_queue):
        ProtocolWorker.__init__(self, conn_queue)

    def execute_protocol_logic(self, conn, client_addr):
        print "[HttpProtocolWorker] handling new HTTP connection"
        http_req = ""
        data = bytearray(1024)
        while not http_req.endswith("\r\n\r\n"):
            print "[HttpProtocolWorker] reading some data from client"
            read_bytes = conn.recv_into(data, 1024)
            if read_bytes == 0:
                print "[HttpProtocolWorker] connection lost!"
                return
            http_req += data[:read_bytes]
        print "[HttpProtocolWorker] got all the data we need."
        conn.sendall("HTTP/1.0 200 Ok\r\nServer: HTTPDan\r\n\r\n<html><body><p>Your Request</p><pre>" + http_req + "</pre></body></html>\r\n\r\n")
        print "[HttpProtocolWorker] done"


if __name__ == "__main__":
    global_conn_queue = Queue.Queue()
    worker = HttpProtocolWorker(global_conn_queue)
    server = SocketServer(global_conn_queue)
    worker.start()
    server.start()
