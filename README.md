# Relcuse

![recluse](https://github.com/user-attachments/assets/d6ce3003-84f1-4554-a2bc-639edbafb0e2)

## Prerequisites

Before you can run this project, you will need the following:
- Python 3.x installed on your machine
- Access to command-line or terminal
- Required Python libraries: `socket`, `threading`, `os`, `random`, `re`, `string`

## Setup

To set up and run this project, follow these steps:

1. Ensure all required Python modules are installed. Most of them are built-in except for a few which might require installation via pip.
2. Clone the repository or download the source code to your local machine.
3. Navigate to the directory containing the script.

## Usage

Run the script using Python from the command line:

```bash
git clone https://github.com/SilentisVox/Recluse
cd Recluse
python Recluse.py
```

![image](https://github.com/user-attachments/assets/5a07b56d-cc88-4ce4-a320-86f79c0a0454)

### Features



---


# Recluse

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

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/recluse.git
   cd recluse
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the main script**
   ```bash
   python Recluse.py
   ```

## Usage

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

---

### Disclaimer

Recluse is intended for **educational and authorized** penetration testing purposes only. Unauthorized use is illegal and punishable by law.

---

### License

This project is not licensed under any open-source agreement and follows the **Non-Apache License Version 1.0**.

---

### Author

Developed by **Silentis Vox** while at **Mandiant**. More details at: [http://www.silentisvox.com](http://www.silentisvox.com)

