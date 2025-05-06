import core.TextAssets

class CommandHandler:
    def __init__(self, generator, networklistener, stagerlistener, connectionhandler, settings):
        self.generator                  = generator
        self.networklistener            = networklistener
        self.stagerlistener             = stagerlistener
        self.instance_networklistener   = None
        self.instance_stagerlistener    = None
        self.connectionhandler          = connectionhandler
        self.connectionhandler_client   = None
        self.settings                   = settings
        self.commands                   = {
            ""                          : self.nothing,
            "help"                      : self.get_help,
            "clear"                     : self.clear,
            "set"                       : self.set_options,
            "start"                     : self.start_job,
            "join"                      : self.join_session,
            "kill"                      : self.kill_job,
            "generate"                  : self.generate_payload
        }

    # These fucntions will help us handle any user input.

    # Simply return if no input.
    def nothing(self):
        return

    # Print help menu.
    def get_help(self):
        print(core.TextAssets.help_menu)

    # Flush the terminal.
    def clear(self):
        core.TextAssets.flush()

    # Set options used for listeners / payloads.
    def set_options(self):
        network_listener_port           = input("> Listening Port: ")

        if not self.verify_port(network_listener_port):
            return

        callback_ip                     = input("> Callback IP: ")

        if not self.verify_ip(callback_ip):
            return

        callback_port                   = input("> Callback Port: ")

        if not self.verify_port(callback_port):
            return

        self.settings.network_listener_address = ("0.0.0.0", int(network_listener_port))
        self.settings.callback_address  = (callback_ip, int(callback_port))

        payload_type                    = input("> Payload Type (script, shell, exe): ")
        payload_name                    = input("> Payload Name: ")

        if not self.verify_payload(payload_type):
            return

        self.settings.payload            = payload_type
        self.settings.payload_name       = payload_name

        return

    # Instantiate a new class object with specified settings.
    def start_job(self):
        job_choice                      = input("> Job (listerner, stager): ")

        if job_choice == "listener":
            self.instance_networklistener = self.networklistener(self.settings)
            self.instance_networklistener.startup_server()

        if job_choice == "stager":
            self.instance_stagerlistener = self.stagerlistener(self.settings)
            self.instance_stagerlistener.startup_server()

    # Begin server / client communication.
    def join_session(self):
        if self.connectionhandler_client:
            self.connectionhandler_client.start_client_communication()

        networklistener_client          = None
        stagerlistener_client           = None

        if self.instance_networklistener:
            networklistener_client      = self.instance_networklistener.client

        if self.instance_stagerlistener:
            stagerlistener_client       = self.instance_stagerlistener.client

        if not self.networklistener.client and not self.stagerlistener.client:
            print("No client connected.")
            return

        if networklistener_client:
            self.connectionhandler_client = self.connectionhandler(networklistener_client)
            self.connectionhandler_client.start_client_communication()

        if stagerlistener_client:
            self.connectionhandler_client = self.connectionhandler(stagerlistener_client)
            self.connectionhandler_client.start_client_communication()

    # Kills all listeners / clients.
    def kill_job(self):
        info                            = core.TextAssets.plus

        print(f"{info} Killing all jobs ...")

        if isinstance(self.instance_networklistener, core.NetworkListener.NetworkListener):
            self.instance_networklistener.shutdown_server()
            self.instance_networklistener.client = None

        if isinstance(self.instance_stagerlistener, core.StagerListener.StagerListener):
            self.instance_stagerlistener.shutdown_server()
            self.instance_stagerlistener.client = None
        
        self.connectionhandler_client   = None

    # Generates static payload with specified settings.
    def generate_payload(self):
        info                            = core.TextAssets.plus

        generator                       = self.generator(self.settings)
        payload                         = generator.generate_payload()
        payload_name                    = self.settings.payload_name

        print(f"{info} Saving payload to '{payload_name}'.")

        write_method                    = ""

        if isinstance(payload, str):
            write_method                = "w"
        else:
            write_method                = "wb"

        open(payload_name, write_method).write(payload)

    # Handle any commands that are not recognized.
    def throw_error(self, command):
        error                           = f"'{command}' is not recognized as a command. Type 'help' for help."
        print(error)

    # Continuously read commands.
    def read_input(self, command):
        if command.lower() not in self.commands:
            self.throw_error(command)
            return

        self.commands[command]()

    def verify_ip(self, ip):
        try:
            ip_octets                       = ip.split(".")
            ip_octets                       = [int(i) for i in ip_octets]
            
            for i in ip_octets:
                if i not in range(256):
                    return False

            return True

        except:
            return False

    def verify_port(self, port):
        try:
            port                        = int(port)
            return port in range (65536)

        except:
            return False

    def verify_payload(self, payload):
        valid_payloads                  = [
            "script",
            "shell",
            "exe"
        ]

        if payload not in valid_payloads:
            return False

        return True
