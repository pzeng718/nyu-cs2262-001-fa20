from flask import Flask, request, abort, jsonify
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def handle_register_put():
    data = request.get_json()

    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not (hostname and ip and as_ip and as_port):
        return jsonify({"error": "Missing required fields"}), 400

    registration_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"

    try:
        send_udp_message(as_ip, int(as_port), registration_message)
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to send registration: {str(e)}"}), 500

def send_udp_message(as_ip, as_port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode('utf-8'), (as_ip, as_port))
    finally:
        sock.close()

@app.route('/fibonacci')
def handle_fibonacci_query():
    number = request.args.get('number')
    if number is None or not number.isdigit():
        abort(400)

    number = int(number)
    
    def calculate_fibonacci(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    return f"{calculate_fibonacci(number)}", 200

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
