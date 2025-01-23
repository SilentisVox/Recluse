import core.TextAssets
import threading

# This handle any client connection. We can send and recieve
# information within an individual connection.
class ConnectionHandler:
    def __init__(self, client):
        self.client                     = client
        self.client_thread              = None
        self.close_connection           = False
        
    def recvall(self): 
        while not self.shutdown:
            try:
                data                    = ""
                while True:
                    part                = self.client.recv(1024).decode()
                    data               += part
                    if len(part) < 1024:
                        break
                print(data, end="", flush=True)
            except:
                print(f"Connection Reset. Press Anything to continue . . . ")
                self.shutdown           = True
                break

    def send_commands(self):
        info                           = core.TextAssets.plus
        while not self.shutdown:
            try:
                command                = input() + "\n"
                self.client.send((command).encode())
            except KeyboardInterrupt:
                print(f"\n{info} Backgrounding Session.")
                break
            except:
                break

    def start_client_communication(self):
        self.client_thread              = threading.Thread(target=self.recvall)
        self.shutdown                   = False
        self.client_thread.daemon       = True
        self.client_thread.start()
        self.send_commands()
        self.shutdown                   = False