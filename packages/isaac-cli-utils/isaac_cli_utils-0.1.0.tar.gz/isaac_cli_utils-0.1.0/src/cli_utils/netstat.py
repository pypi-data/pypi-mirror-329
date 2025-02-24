import subprocess
import re
import platform
from rich.console import Console
from rich.table import Table

def get_connections():
    # Detect OS
    os_type = platform.system().lower()

    if os_type == 'linux':
        # Linux netstat command
        cmd = """netstat -tunlp | grep LISTEN | awk '{split($NF,a,"/"); printf "proto: %s | addr.port: %s | pid: %s | name: %s\n", $1, $4, a[1], a[2]}'"""
    else:
        # macOS netstat command 
        cmd = """netstat -Watnlv | grep LISTEN | awk '{"ps -o comm= -p " $9 | getline procname; print "proto: " $1 " | addr.port: " $4 " | pid: " $9 " | name: " procname;  }'"""
    
    output = subprocess.check_output(cmd, shell=True, text=True)
    print(output)
    
    # Parse the output into list of dicts
    connections = {}  # Using dict with pid as key to group by process
    for line in output.splitlines():
        if not line.strip():
            continue
            
        # Extract fields using regex
        match = re.match(r'proto:\s+(\S+)\s+\|\s+addr\.port:\s+(\S+)\s+\|\s+pid:\s+(\d+)\s+\|\s+name:\s+(.+)$', line.strip())
        if match:
            proto, addr_port, pid, name = match.groups()
            pid = int(pid)
            
            # Split address and port, handling both .port and :port formats
            if '.' in addr_port:
                # Handle format like "127.0.0.1.8000" or "*.8000"
                parts = addr_port.split('.')
                port = parts[-1]  # Last part is always the port
                addr = '.'.join(parts[:-1]) if addr_port[0] != '*' else '*'
            else:
                # Handle format like "::1:8000"
                try:
                    addr, port = addr_port.rsplit(':', 1)
                except ValueError:
                    addr = '*'
                    port = addr_port

            # If pid already exists, append the port to its ports list
            if pid in connections:
                if port not in connections[pid]['ports']:
                    connections[pid]['ports'].append(port)
            else:
                connections[pid] = {
                    'proto': proto,
                    'addr': addr,
                    'ports': [port],
                    'pid': pid,
                    'name': name.strip()
                }
    
    return list(connections.values())

def print_connections(connections):

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    
    table.add_column("Protocol", style="dim")
    table.add_column("Address")
    table.add_column("Ports")
    table.add_column("PID", justify="right")
    table.add_column("Process Name")

    for conn in connections:
        table.add_row(
            conn['proto'],
            conn['addr'],
            ", ".join(conn['ports']),
            str(conn['pid']),
            conn['name']
        )

    console.print(table)

def main():
    connections = get_connections()
    print_connections(connections)

if __name__ == "__main__":
    main()
