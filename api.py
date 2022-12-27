import os
from urllib import request

from flask import Flask, request

os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']
from main import main

app = Flask(__name__)

@app.route('/')
def main_route():
    print(f'Received request from {request.remote_addr}, forwarding to main.py')
    return main()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
    )
