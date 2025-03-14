import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')  # Fallback if not in .env

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

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
    username = user_info['login']
    email = user_info.get('email')  # Might be None if not public

    # Save or update user in database
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email)
            db.session.add(user)
        else:
            user.email = email  # Update email if changed
        db.session.commit()

    session['user'] = username  # Store username in session
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/update-section')
@login_required
def update_section():
    return render_template('partial.html')

@app.route('/users')
@login_required
def list_users():
    users = User.query.all()
    return '<br>'.join([f"Username: {u.username}, Email: {u.email}" for u in users])

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)