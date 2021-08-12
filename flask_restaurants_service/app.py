from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello, flask-world!'


if __name__ == '__main__':
    app.run(port='4800', host='0.0.0.0')