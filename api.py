import os

from flask import Flask

os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']
from main import main

app = Flask(__name__)


@app.route('/')
def root():
    return main()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        threaded=True,
    )
