import asyncio
import logging
import socket
import psutil
import json
import sys
import os
import time
import functools
from collections import defaultdict
import concurrent.futures

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def scan_tcp_port(port: int, address: str, timeout=1):
    try:
        conn = asyncio.open_connection(address, port)
        _, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return "Open"
    except asyncio.TimeoutError:
        return "Filtered"
    except ConnectionRefusedError:
        return "Closed"
    except Exception as e:
        return f"Error: {str(e)}"


async def scan_udp_port(port: int, address: str, timeout=1):
    loop = asyncio.get_running_loop()
    try:
        transport, _ = await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(), remote_addr=(address, port)
        )
        transport.sendto(b"\x00")
        await asyncio.sleep(timeout)
        transport.close()
        return "Open|Filtered"
    except Exception:
        return "Closed|Filtered"


def get_existing_connections():
    connections = defaultdict(list)
    for conn in psutil.net_connections(kind="all"):
        if conn.laddr:
            if isinstance(conn.laddr, tuple):
                port = conn.laddr[1]
            elif hasattr(conn.laddr, "port"):
                port = conn.laddr.port
            else:
                continue
            connections[port].append(
                {
                    "type": conn.type,
                    "status": conn.status,
                    "pid": conn.pid,
                    "family": conn.family,
                    "laddr": conn.laddr,
                    "raddr": conn.raddr if conn.raddr else None,
                }
            )
    return connections


async def scan_ports(
    start_port=1, end_port=65535, timeout=1, address="127.0.0.1", max_concurrent=500
):
    logger.info(
        f"Starting comprehensive port scan on {address} from port {start_port} to {end_port}"
    )
    logger.debug(
        f"Scanning ports {start_port} to {end_port} on {address} with timeout {timeout} and max concurrent scans {max_concurrent}"
    )

    sem = asyncio.Semaphore(max_concurrent)
    existing_connections = get_existing_connections()

    async def scan_with_semaphore(port):
        async with sem:
            logger.debug(f"Scanning TCP port {port} on {address}")
            tcp_status = await scan_tcp_port(port, address, timeout)
            logger.debug(f"Scanning UDP port {port} on {address}")
            udp_status = await scan_udp_port(port, address, timeout)
            return port, tcp_status, udp_status

    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        scan_tasks = [
            scan_with_semaphore(port) for port in range(start_port, end_port + 1)
        ]
        results = await asyncio.gather(*scan_tasks)

        def process_result(result):
            port, tcp_status, udp_status = result
            existing_info = existing_connections.get(port, [])
            return port, tcp_status, udp_status, existing_info

        processed_results = await asyncio.gather(
            *[loop.run_in_executor(pool, process_result, result) for result in results]
        )

    logger.info(
        f"Port scan completed on {address}. Scanned {len(processed_results)} ports."
    )
    return processed_results


@functools.lru_cache(maxsize=None)
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"


async def get_process_details(pid, light_mode=False):
    try:
        proc = psutil.Process(pid)
        if light_mode:
            return f"Process: {proc.name()} (PID: {pid})"
        else:
            create_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time())
            )
            return (
                f"Process: {proc.name()} (PID: {pid}), Executable: {proc.exe()}, "
                f"Command: {' '.join(proc.cmdline())}, User: {proc.username()}, "
                f"Create Time: {create_time}"
            )
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "Process details unavailable"


async def get_service_details(
    port, tcp_status, udp_status, existing_info, address, sem, light_mode=False
):
    async with sem:
        logger.debug(f"Getting service details for port {port} on {address}")

        service = get_service_name(port)

        details = []
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            detail_futures = []
            for conn in existing_info:
                conn_details = f"Family: {conn['family'].name}, Type: {conn['type'].name}, Status: {conn['status']}"
                if conn["pid"]:
                    detail_futures.append(
                        loop.run_in_executor(
                            pool,
                            asyncio.run,
                            get_process_details(conn["pid"], light_mode),
                        )
                    )
                else:
                    details.append(conn_details)

            process_details = await asyncio.gather(*detail_futures)
            details.extend(
                [
                    f"{d}, {pd}"
                    for d, pd in zip(
                        [d for d in details if "Process details unavailable" not in d],
                        process_details,
                    )
                ]
            )

        if not details:
            details.append("No additional details found")

        logger.debug(
            f"Service details for port {port} on {address}: {service}, {len(details)} connection(s)"
        )
        return {
            "port": port,
            "service": service,
            "tcp_status": tcp_status,
            "udp_status": udp_status,
            "details": details,
        }


async def service_report(
    all_ports, address: str, max_concurrent: int, light_mode: bool
):
    logger.info(f"Generating service report for {address}")
    sem = asyncio.Semaphore(max_concurrent)
    tasks = [
        get_service_details(
            port, tcp_status, udp_status, existing_info, address, sem, light_mode
        )
        for port, tcp_status, udp_status, existing_info in all_ports
    ]
    results = await asyncio.gather(*tasks)
    logger.info(f"Service report completed for {len(results)} ports on {address}")
    return results


def save_to_file(data, filename):
    logger.info(f"Saving results to file: {filename}")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    logger.info("Results saved successfully")


def check_privileges():
    try:
        return os.geteuid() == 0
    except AttributeError:
        # OS doesn't support geteuid (e.g., Windows)
        return False


async def run_scan(
    start_port,
    end_port,
    output_file,
    timeout,
    address,
    debug,
    max_concurrent,
    privileged,
    light_mode,
):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode activated")

    if privileged and not check_privileges():
        logger.warning(
            "Privileged mode requested but script is not running with elevated permissions."
        )
        logger.warning("Some operations may fail. Consider running with sudo.")

    if start_port < 1024 and not check_privileges():
        logger.warning(
            "Scanning privileged ports (below 1024) may require elevated permissions."
        )
        logger.warning("Some scans might fail or provide incomplete results.")

    logger.info(f"Starting comprehensive scan on {address}")
    all_ports = await scan_ports(start_port, end_port, timeout, address, max_concurrent)

    logger.info(f"Gathering service details for {address}...")
    services = await service_report(all_ports, address, max_concurrent, light_mode)

    logger.info(f"Services and sockets on all scanned ports for {address}:")
    for service in services:
        logger.info(f"Port: {service['port']} - Service: {service['service']}")
        logger.info(f"  TCP: {service['tcp_status']}, UDP: {service['udp_status']}")
        for detail in service["details"]:
            logger.info(f"  Detail: {detail}")

    if output_file:
        save_to_file(services, output_file)

    return services


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Scan all ports and identify services")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument(
        "--end", type=int, default=65535, help="End port (default: 65535)"
    )
    parser.add_argument(
        "--output", type=str, help="Output file for results (JSON format)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1,
        help="Timeout for each port scan (default: 1 second)",
    )
    parser.add_argument(
        "--address",
        type=str,
        default="127.0.0.1",
        help="Specify an IPv4 or IPv6 address to scan",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=500,
        help="Maximum number of concurrent scans (default: 500)",
    )
    parser.add_argument(
        "--privileged",
        action="store_true",
        help="Run in privileged mode (requires elevated permissions)",
    )
    parser.add_argument(
        "--light",
        action="store_true",
        help="Run in light mode for faster scans with less detail",
    )
    args = parser.parse_args()

    if args.max_concurrent > 1000:
        logger.warning(
            f"Very high concurrency ({args.max_concurrent}) may impact system stability. Consider a lower value."
        )

    asyncio.run(
        run_scan(
            args.start,
            args.end,
            args.output,
            args.timeout,
            args.address,
            args.debug,
            args.max_concurrent,
            args.privileged,
            args.light,
        )
    )


if __name__ == "__main__":
    main()
