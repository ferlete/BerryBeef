import sys
import threading
import socket

from BERRYBEEF.constants import *

class Client:

    def __init__(self):
        super().__init__()
        self.server_address = ()
        # create socket TCP
        self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketClient.settimeout(5)  # 5 seconds

        # allow python to use recently closed socket
        self.socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def connect(self, ip, port):
        try:
            self.server_address = (ip, int(port))

            # Connect the socket to the port where the server is listening
            self.socketClient.connect(self.server_address)
            print(self.socketClient)
            if not self.socketClient:
                return False
            else:
                return True

        except Exception as ex:
            print(ex)

    def retr_file(self):

        filename = "model.csv"
        with open(filename, 'wb') as f:
            print("[+] filename open %s" % filename)
            data = self.socketClient.recv(BUFFER_SIZE)
            #print("[+] received file %s from %s" % (self.filename, addr))
            print('data=%s', (data))

            #buffer_data = data

            try:
                while (data):
                    f.write(data)
                    data = self.socketClient.recv(BUFFER_SIZE)
                    print("received message: %s" % data)
                self.socketClient.close()
                print("[+] File Downloaded")
                f.close()
                self.socketClient.close()

            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)

