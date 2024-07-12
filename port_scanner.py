import re
import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    error_string = 'Error: Invalid hostname' if((not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target)) and (re.match(r"^[a-zA-Z0-9\-.]+$", target))) else 'Error: Invalid IP address'
    #print(f'Error would be: {error_string}')
    for port in range(port_range[0], port_range[1] + 1):
        # 'with' opens socket as 's', and handles closing socket as well
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #s.settimeout(1)
            s.settimeout(1)
            try:
                if not s.connect_ex((target, port)):
                    open_ports.append(port)
            # socket.gaierror provide specific errors for invalid hostnames or IP addresses
            except (socket.gaierror, ValueError) as e:
                # Provide error for host, or IP address given
                return error_string

    # Only return list of open ports
    if not verbose:
        return open_ports
    
    ip = socket.gethostbyname(target)
    host = None
    try: 
      host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
      host = None
    
    # Assemble return string
    gap=9 #number of chars before SERVICE
    string = f'Open ports for {host} ({ip})' if not host == None else f'Open ports for {ip}'
    string += '\nPORT     SERVICE'
    for port in open_ports:
        if port in ports_and_services:
            # print(ports_and_services[port])
            string += '\n' + str(port) + (' ' * (gap - len(str(port)))) + ports_and_services[port]
        else:
            string += '\n' + str(port)

    return string