
from flask import Flask, render_template
from netmiko import ConnectHandler
from pathlib import Path
import os

app = Flask(__name__)

# Router configuration
router_device = {
    'device_type': 'cisco_ios_telnet',
    'ip': os.getenv('ROUTER_IP', '192.168.10.122'),
    'port': int(os.getenv('ROUTER_PORT', '32770')),
    'username': os.getenv('ROUTER_USERNAME', 'admin'),
    'password': os.getenv('ROUTER_PASSWORD', 'eve'),
    'secret': os.getenv('ROUTER_SECRET', 'YOUR_ENABLE_SECRET'),
}

# Commands to execute
command_to_run = [
    'show version',
    'show ip interface brief',
    'show running-config'
]


@app.route('/')
def index():

    result = {}
    error = None

    try:
        print("Connecting to the router...")

        net_connect = ConnectHandler(**router_device)

        net_connect.enable()

        for cmd in command_to_run:

            print(f"\nExecuting: {cmd}")

            output = net_connect.send_command(cmd)

            result[cmd] = output

        net_connect.disconnect()

        print("Connection closed successfully.")

    except Exception as e:
        error = f"Connection failed: {e}"
        print(error)

    return render_template(
        'index.html',
        result=result,
        error=error,
        router=router_device
    )


@app.route('/view-code')
def view_code():
    html_file = Path(app.root_path) / 'templates' / 'index.html'

    with open(html_file, 'r', encoding='utf-8') as file:
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
