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
            #print(self.socketClient)
            if not self.socketClient:
                return False
            else:
                return True

        except Exception as ex:
            print(ex)

    def retr_file(self):

        with self.socketClient, self.socketClient.makefile('rb') as clientfile:
            while True:
                raw = clientfile.readline()
                if not raw: break  # no more files, server closed connection.

                filename = raw.strip().decode()
                length = int(clientfile.readline())
                print(b'Downloading {filename}...\n  Expecting {length:,} bytes...', end='', flush=True)

                path = os.path.join('', filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                # Read the data in chunks so it can handle large files.
                with open(path, 'wb') as f:
                    while length:
                        chunk = min(length, BUFFER_SIZE)
                        data = clientfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
                    else:  # only runs if while doesn't break and length==0
                        print('Complete')
                        continue

                # socket was closed early.
                print('Incomplete')
                break