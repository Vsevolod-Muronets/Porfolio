from flask import Flask

applic = Flask(__name__)

@applic.route('/')
def hello_w():
    return 'Hello, World!'