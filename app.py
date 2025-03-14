from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this in production!

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/update-section')
def update_section():
    return render_template('partial.html')

if __name__ == '__main__':
    app.run(debug=True)