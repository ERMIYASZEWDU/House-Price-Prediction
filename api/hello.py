from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/api/hello')
def hello():
    return {'message': 'Hello from Vercel!', 'status': 'working'}
