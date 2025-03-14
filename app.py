from flask import Flask, render_template, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from functools import wraps
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this in production!

# OAuth setup
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return "<p>Please <a href='/login'>log in</a> with GitHub.</p>"
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    user = session.get('user')
    return render_template('base.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    user_info = resp.json()
    session['user'] = user_info['login']  # Store username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/update-section')
@login_required
def update_section():
    return render_template('partial.html')

if __name__ == '__main__':
    app.run(debug=True)