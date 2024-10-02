from flask import Flask, request, abort, jsonify
import requests
from socket import socket, AF_INET, SOCK_DGRAM
app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def handle_fibonacci_get():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    registration_message = f"TYPE=A\nNAME={hostname}"

    try:
        result = send_udp_message(as_ip, int(as_port), registration_message)
        ip_address = [line.split('=')[1] for line in result.splitlines() if line.startswith("VALUE=")][0]
        response, code = send_get_request(f"http://{ip_address}:9090", number)

        return response, 200
    except Exception as e:
        return jsonify({"error": f"Failed to query AS: {str(e)}"}), 500


def send_udp_message(as_ip, as_port, msg):
    print(f"{as_ip}, {as_port}")
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)
        client_socket.sendto(msg.encode(), (as_ip, as_port))
        
        try:
            response, _ = client_socket.recvfrom(2048)
            return response.decode()
        except Exception as e:
            raise e

def send_get_request(url, number):
    target_url = f"{url}/fibonacci?number={number}"
    
    response = requests.get(target_url)
    
    return jsonify(response.json()), response.status_code

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
