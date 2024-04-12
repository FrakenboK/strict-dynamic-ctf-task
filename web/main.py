from flask import Flask, request, render_template, redirect, url_for, session, make_response
import random, hashlib, time, asyncio, bot, json, os
from config import config
from utils import nonce

app = Flask(
    'strict',
    static_folder='static',
    template_folder='templates'
)

config = config.Config()

app.secret_key = config.session_key

def render_with_csp(template):
    nonce_value = nonce.generate(config.nonce_secret)
    resp = make_response(render_template(template, nonce=nonce_value))
    resp.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce_value}' 'strict-dynamic'; image-src 'none'; style-src 'self'; iframe-src 'none'"
    return resp

@app.route('/index')
def index():
    if 'username' in session:
        return redirect(url_for('add_note'))
    return redirect(url_for("login", error='You are not logged in'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('add_note'))
    
    if request.method == 'GET':
        return render_with_csp("register.html")

    username = request.form.get('username')
    password = request.form.get('password')

    if not (0 < len(username) < 20 and 0 < len(password) < 20):
        return redirect(url_for('register', error='Invalid username or password'))

    if username in os.listdir("users"):
        return redirect(url_for('register', error='User already exists'))

    with open("users/" + os.path.basename(username), 'w', encoding='utf-8') as file:
        user = dict()
        user['password'] = hashlib.md5(password.encode()).hexdigest()
        user['time_created'] = str(int(time.time()))
        user['my_notes'] = []

        json.dump(user, file, ensure_ascii=False, indent=4)

    session['username'] = username
    return redirect(url_for("add_note", message='Register succesfull'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('add_note'))
    
    if request.method == 'GET':
        return render_with_csp("login.html")

    username = request.form.get('username')
    password = request.form.get('password')

    username = os.path.basename(username)
    if not (0 < len(username) < 20 and 0 < len(password) < 20):
        return redirect(url_for('login', error='Invalid username or password'))

    if username not in os.listdir("users"):
        return redirect(url_for('login', error='No such user'))

    with open("users/" + username, 'r') as file:
        info = json.loads(file.read())
        if hashlib.md5(password.encode()).hexdigest() != info['password']:
            return redirect(url_for('login', error='Invalid password'))
    
    session['username'] = username
    return redirect(url_for("add_note", message='Login succesfull'))
    
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_with_csp("add_note.html")

@app.route('/notes')
def notes():
    # общий список
    return "notes"

@app.route('/my')
def my():
    # только мои с возможностью чтения доп полей
    return "my"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/visit')
async def visit_web():
    await bot.visit()
    return "visited"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=False)