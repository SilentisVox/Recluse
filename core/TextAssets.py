import os

def bold(text):
    return "\033[1m{}\033[0m".format(text)

def underline(text):
    return "\033[4m{}\033[0m".format(text)

def white(text):
    return "\x1b[38;2;255;255;255m{}\x1b[0m".format(text)

def brown(text):
    return "\x1b[38;2;88;44;0m{}\x1b[0m".format(text)

def flush():
    os.system('cls')

recluse_banner                          = f"""
                             ░░░░░░░░░░░
                          ░▒▓░░
                       ░░▓▒░             ░░░░░░░░░
                 ░░░░░░█░░          ░░▒▒░░░
                ░█░   ▓▒         ░▒▒▒░░
                █░   ░█░      ░▓▓▒░
                ░█░░ ░█░   ░▒█▒░         
          ░░░░░░ ░▒▓░▒█░ ░▒▓▒░             
        ░░▒▓░░▓▓▓▓▒██████▓█▒▒▒▒▒▒░░░░░░░   {white("┳━━━┓ ┏━━━┓ ┏━━━┓ ┳    ┳   ┳ ┏━━━┓ ┏━━━┓")}
    ░░▓▓▒▒░▓███████████▓█▓░░               {white("┃   ┃ ┃     ┃     ┃    ┃   ┃ ┃     ┃    ")}
 ░▒▓▓░░    █████████▓██░                   {white("┣━┳━┛ ┣━━━  ┃     ┃    ┃   ┃ ┗━━━┓ ┣━━━ ")}
░▓░        ███████▓░██░▓                   {white("┃ ┗┓  ┃     ┃     ┃    ┃   ┃     ┃ ┃    ")}
░▓         ░░▓█▓▒░ ░▓░ ░▓                  {white("┻  ┻━ ┗━━━┛ ┗━━━┛ ┗━━┛ ┗━━━┛ ┗━━━┛ ┗━━━┛")}
░▓                 █▓   ░░                 {brown("                         S I L E N T I S")}
░░                ░█░
                  ▓▓
                  ▓░
                 ░█
                 ░▒
                 ▒░
                 ░
"""

recluse_colors                          = [
    (66, 33, 0),
    (64, 32, 0),
    (63, 31, 0),
    (62, 31, 0),
    (61, 30, 0),
    (59, 29, 0),
    (58, 29, 0),
    (57, 28, 0),
    (56, 27, 0),
    (54, 27, 0),
    (53, 26, 0),
    (52, 25, 0),
    (51, 25, 0),
    (49, 24, 0),
    (48, 23, 0),
    (47, 23, 0),
    (46, 22, 0),
    (44, 21, 0),
    (43, 21, 0),
    (42, 20, 0),
    (41, 20, 0)
]

def banner():
    recluse_lines                       = recluse_banner.split("\n")
    recluse_colored                     = ""

    for line, color in zip(recluse_lines, recluse_colors):
        color_code                      = f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"
        end_code                        = "\x1b[0m"
        recluse_colored                += color_code + line + end_code + "\n"

    return recluse_colored

prompt                                  = white(bold(underline("Recluse") + " > "))
plus                                    = brown("[*]")
exclam                                  = brown("[!]")

help_menu                               = f"""

    {plus} help        :: Will display this help menu.
    {plus} set         :: Run this command to set all options for C2.
    {plus} start       :: Run this command to start a listener.
    {plus} join        :: Run this to join a session.
    {plus} kill        :: Run this to kill all listeners.
    {plus} generate    :: Run this to generate a payload with specified settings.

"""