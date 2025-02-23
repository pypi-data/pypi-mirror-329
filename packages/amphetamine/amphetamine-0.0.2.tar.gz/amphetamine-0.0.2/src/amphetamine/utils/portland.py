import socket


def scan_port(ip: str, port: int) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except socket.error as e:
        print(f"Socket error: {e}")
        return False


def scan_ports(ip: str, ports):
    open_ports = []
    for port in ports:
        print(f"Scanning port {port}...")
        if scan_port(ip, port):
            print(f"Port {port} is open.")
            open_ports.append(port)
        else:
            print(f"Port {port} is closed or blocked.")
    return open_ports


def main(target_ip: str, ports):
    print(f"Scanning ports on {target_ip}...")
    open_ports = scan_ports(target_ip, ports)

    if 80 in open_ports:
        print("Port 80 is open.")
    else:
        print("Port 80 is closed or blocked.")

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(f"Port {port} is open.")
    else:
        print("No open ports found in the specified range.")


if __name__ == "__main__":
    target_ip = input("Enter the IP address to scan: ")
    port_input = input(
        "Enter the port or range of ports to scan (e.g., '80' or '1-1024'): "
    )

    if "-" in port_input:
        start_port, end_port = map(int, port_input.split("-"))
        ports = range(start_port, end_port + 1)
    else:
        ports = [int(port_input)]

    main(target_ip, ports)
