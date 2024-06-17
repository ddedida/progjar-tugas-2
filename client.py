import socket
import logging
import threading
import time

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("Open socket")

    server_address = ('0.0.0.0', 45001)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        while True:
            message = input('Input message here: ')
            if message == 'QUIT':
                break
            logging.warning(f"[CLIENT] sending {message}")
            sock.sendall(message.encode())

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = sock.recv(32)
                amount_received += len(data)
                logging.warning(f"[SERVER] {data.decode('utf-8')}")
    finally:
        logging.warning("closing")
        sock.close()
    return

if __name__ == '__main__':
    threads = []
    startTime = time.time()

    t = threading.Thread(target=kirim_data)
    threads.append(t)

    for thr in threads:
        thr.start()
        thr.join()
