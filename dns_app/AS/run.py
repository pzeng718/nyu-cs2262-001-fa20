import socket
import json

dns_records = {}

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('0.0.0.0', 53533))
        while True:
            data, addr = sock.recvfrom(1024)
            parts = [item.split('=')[1] for item in data.decode().split('\n') if item]
            dns_type = parts[0]
            print("message received:", parts)
            if len(parts) == 4: # register
                [_, dns_name, dns_ip, dns_ttl] = parts 
                if(dns_type not in dns_records): 
                    dns_records[dns_type] = {}
                dns_records[dns_type][dns_name] = (dns_ip, dns_ttl)
                print(f'Registered {dns_name} -> {dns_ip} wtih TTL {dns_ttl}')
            elif len(parts) == 2:  # query
                [_, dns_name] = parts
                if dns_type in dns_records and dns_name in dns_records[dns_type]:
                    dns_ip, dns_ttl = dns_records[dns_type][dns_name]
                    response = f"TYPE={dns_type}\nNAME={dns_name}\nVALUE={dns_ip}\nTTL={dns_ttl}"
                    sock.sendto(response.encode(), addr)
                    print(f'Returned {dns_name} -> {dns_ip}:{dns_ttl}')
                else:
                    response = f"TYPE={dns_type}\nNAME={dns_name}\nHOST_NOT_FOUND"
                    sock.sendto(response.encode(), addr)
                    print(f'Hostname {dns_name} not found')
            else:
                print('Invalid data format')


if __name__ == '__main__':
    udp_server()