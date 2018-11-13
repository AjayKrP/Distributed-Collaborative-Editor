from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from flask_socketio import SocketIO
import redis

FILE_LIST_KEY = 'files'

app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t!@#$'
socketio = SocketIO(app)

r = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/delete/<name>')
def delete_file(name):
    r.lrem(FILE_LIST_KEY, 0, name)
    return redirect('/view_files')


@app.route('/create_file', methods=['POST'])
def create_file():
    file_name = request.form['file_name']
    r.lpush(FILE_LIST_KEY, file_name)
    r.set(file_name, "")
    return redirect('/view_files')


@app.route('/view_files')
def view_files():
    files = list(map(lambda x: x.decode(), r.lrange(FILE_LIST_KEY, 0, -1)))
    return render_template('list_files.html', files=files)


@app.route('/edit/<name>')
def edit_file(name):
    content = r.get(name)
    if content: content = content.decode()
    return render_template('edit_file.html', content=content, file_name=name)


@app.route('/save_file', methods=['POST'])
def save_file():
    if request.method == 'POST':
        file_name = request.form['file_name']
        r.set(file_name, request.form[file_name])
        return redirect('/view_files')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        session['nickname'] = request.form['nickname']
        return redirect('/view_files')


@socketio.on('update')
def handle_message(message):
    socketio.emit('updated_text', message, include_self=False)


@socketio.on('delete')
def delete_text():
    print("delete")


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 5000)
