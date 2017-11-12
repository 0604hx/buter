import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/time')
def show_time():
    """
    返回当前时间，格式为：yyyy-MM-dd HH:mm:ss
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True)