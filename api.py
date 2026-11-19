
from flask import Flask, render_template, jsonify
from netmiko import ConnectHandler
import os

app = Flask(__name__)

# Router configuration
router_device = {
    'device_type': 'cisco_ios_telnet',
    'ip': os.getenv('ROUTER_IP', '192.168.10.122'),
    'port': int(os.getenv('ROUTER_PORT', '32770')),
    'username': os.getenv('ROUTER_USERNAME', 'admin'),
    'password': os.getenv('ROUTER_PASSWORD', 'eve123'),
    'secret': os.getenv('ROUTER_SECRET', 'eve123'),
}

# Diagnostic commands
command_to_run = [
    'show version',
    'show ip interface brief',
    'show running-config'
]


@app.route('/')
def index():
    return render_template('index.html', router=router_device)


@app.route('/run-diagnostics', methods=['POST'])
def run_diagnostics():

    result = {}
    net_connect = None

    try:
        print("Connecting to router...")

        net_connect = ConnectHandler(**router_device)

        net_connect.enable()

        for cmd in command_to_run:
            print(f"Executing: {cmd}")

            output = net_connect.send_command(cmd)
            result[cmd] = output

        print("Connection successful.")

        return jsonify({
            'success': True,
            'outputs': result
        })

    except Exception as e:

        print(f"Connection failed: {e}")

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    finally:
        if net_connect:
            net_connect.disconnect()


@app.route('/view-code')
def view_code():
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        source_code = file.read()

    return render_template(
        'source.html',
        source_code=source_code
    )


if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
