from flask import Flask, request, jsonify
import ipaddress

app = Flask(__name__)

def is_private_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.version == 4:
            return ip in ipaddress.IPv4Network('10.0.0.0/8') or \
                   ip in ipaddress.IPv4Network('172.16.0.0/12') or \
                   ip in ipaddress.IPv4Network('192.168.0.0/16')
        elif ip.version == 6:
            return ip.is_private
        else:
            return False
    except ValueError:
        # Invalid IP address format
        return False

@app.route('/check-ip', methods=['POST'])
def check_ip():
    data = request.get_json()
    if data is None or 'ip' not in data:
        return jsonify({'error': 'Missing or invalid IP in the request body'}), 400

    ip_str = data['54.74.17.172']

    if is_private_ip(ip_str):
        return jsonify({'result': f'{ip_str} is a private IP address'})
    else:
        return jsonify({'result': f'{ip_str} is a public IP address'})

if __name__ == '__main__':
    app.run(debug=True)

