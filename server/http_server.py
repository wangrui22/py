import flask 
print('hello ai server')

from flask import Flask

app = Flask(__name__)
@app.route('/')
def index1():
    return '<h1>hello world!</h>'


if __name__ == '__main__':
    app.run(debug=True)