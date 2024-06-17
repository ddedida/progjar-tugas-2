from socket import *
import socket
import threading
import logging
import time

class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(32)
            if data:
                data = data.decode('utf-8')
                logging.warning(f"[CLIENT] received request")
                if data.startswith('TIME'):
                    currentTime = time.strftime('%H:%M:%S', time.localtime())
                    response = f"Current time: {currentTime}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                    logging.warning(f"[SERVER] send response")
                else:
                    response_error = "ERROR: Invalid request message\r\n"
                    self.connection.sendall(response_error.encode('utf-8'))
                    logging.warning(f"[SERVER] send response")
            else:
                break
        self.connection.close()
        logging.warning(f"Connection close from {self.address}")
        logging.warning(f"Waiting connection on port 45000")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45001))
        self.my_socket.listen(1)
        logging.warning(f"Waiting connection on port 45001")
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"Connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()

if __name__=="__main__":
    main()