from flask import Flask, request, render_template, redirect, url_for, session, make_response
import random, hashlib, time, asyncio
from bot import visit

app = Flask(
    'strict',
    static_folder='static',
    template_folder='templates'
)

@app.route('/index')
def index():
    resp = make_response(render_template('index.html', nonce="123"))
    resp.headers['Content-Security-Policy'] = "script-src 'nonce-123' 'strict-dynamic';"
    return resp

@app.route('/visit')
async def visit_web():
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(visit()) 
    await visit()
    return "visited"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=False)