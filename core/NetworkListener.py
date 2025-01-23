import core.TextAssets

import socket
import threading

# This will be our static listener that we will receive 1 connection
# We will stop listening but preserve the connection.
class NetworkListener:
    client                              = None

    def __init__(self, settings):
        self.settings                   = settings
        self.server_listener            = None
        self.server_shutdown            = threading.Event()
        
    def listen(self):
        info                            = core.TextAssets.plus
        exclam                          = core.TextAssets.exclam
        prompt                          = core.TextAssets.prompt

        try:
            self.server_listener.bind(self.settings.network_listener_address)
            self.server_listener.listen(1)

            NetworkListener.client, address = self.server_listener.accept()

            remote_ip_address           = address[0]
            remote_port_address         = address[1]

            print(f"\n{info} Backdoor connection received from {remote_ip_address}:{remote_port_address}. Type 'join' to join session.\n", end=prompt, flush=True)

        except:
            print(f"{exclam} Listener failed to bind to address.")
            return
    
    def startup_server(self):
        brown                           = core.TextAssets.brown

        if self.server_listener:
            self.server_shutdown()
        self.server_listener            = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_thread              = threading.Thread(target=self.listen)
        self.server_thread.daemon       = True
        self.server_thread.start()

        port_address                    = "[" + str(self.settings.network_listener_address[1]) + "]"
        print(f"Multi Handling Listener {brown(port_address)}")
        
    def shutdown_server(self):
        self.server_shutdown.set()

        if NetworkListener.client:
            NetworkListener.client.close()
            NetworkListener.client      = None

        if self.server_listener:
            self.server_listener.close()

        self.server_listener = None