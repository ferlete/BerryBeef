import sys
import threading
import socket

from BERRYBEEF.constants import *

class Client:

    def __init__(self, ip, port):
        super().__init__()
        self.server_address = (ip, int(port))
        try:
            # create socket TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 seconds

            # allow python to use recently closed socket
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Connect the socket to the port where the server is listening
            print('[+] connecting to %s:%s' % self.server_address)
            self.socket.connect(self.server_address)

            # create to work on a different thread
            i_thread = threading.Thread(target=self.retr_file)
            i_thread.daemon = False
            i_thread.start()

        except Exception as e:
            print(e)
        sys.exit()

    def retr_file(self):

        self.filename = "model.csv"
        print("[+] resquest filename %s" % self.filename)

        f = open(self.filename, 'wb')
        data, addr = self.socket.recv(BUFFER_SIZE)
        print("[+] received file %d from %s" % (self.filename, addr))

        #buffer_data = data

        try:
            while (data):
                f.write(data)
                data, addr = self.socket.recvfrom(BUFFER_SIZE)
                #buffer_data += data
                # print("received message: %s" % data)
            self.socket.close()
            print("[+] File Downloaded")

        except Exception as e:
            print(e)
        sys.exit()
