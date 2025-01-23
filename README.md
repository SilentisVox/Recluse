# Recluse

![recluse](https://github.com/user-attachments/assets/d6ce3003-84f1-4554-a2bc-639edbafb0e2)

Recluse is a lightweight Command and Control (C2) framework designed for remote administration and penetration testing. It provides robust payload generation, obfuscation, and communication capabilities.

## Prerequisites

Before setting up Recluse, ensure you have the following dependencies installed:

- Python 3.8+
- Required Python modules:
  - `socket`
  - `threading`
  - `random`
  - `re`
  - `os`
  - `string`
- A compatible operating system (Linux/macOS/Windows)
- Administrative privileges (for network listener binding)

## Setup

Follow these steps to install and set up Recluse:

   ```bash
   git clone https://github.com/yourusername/recluse.git
   cd recluse
   python Recluse.py
   ```

## Usage

![image](https://github.com/user-attachments/assets/5a07b56d-cc88-4ce4-a320-86f79c0a0454)

Once Recluse is running, you can interact with it using the following commands:

- `help` → Displays the help menu
- `set` → Configures network settings for listeners and payloads
- `start` → Starts a listener (either `listener` or `stager` mode)
- `join` → Connects to an active session
- `kill` → Terminates all active listeners
- `generate` → Creates an obfuscated payload with specified settings

Example Workflow:

```bash
set
> Listening Port: 4444
> Callback IP: 192.168.1.100
> Callback Port: 4444
> Payload Type (script, shell, exe): script
> Payload Name: backdoor.ps1

start
> Job (listener, stager): listener

generate
[*] Saving payload to 'backdoor.ps1'.
```

## Features

- **Command & Control**: Supports multiple commands for managing remote systems.
- **Payload Generation**: Generates `PowerShell`, `Shellcode`, and `EXE` payloads.
- **Obfuscation**: Uses advanced obfuscation techniques to evade detection.
- **Listener Management**: Supports persistent and dynamic listeners.
- **Session Handling**: Allows joining and controlling remote sessions.


