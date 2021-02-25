from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import pandas as pd
from ExtraStuff import encoder,decoder
app = Flask(__name__)
app.secret_key = 'hi'

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/')
def front():
    return render_template('front.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")
        if decoder(df[df['User'] == user]['Pass'].values[0]) == password:
            flash(f'you are logged in {user}')
            return redirect(url_for('front'))
        else:
            flash('wrong username password')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        email = request.form.get('email')
        user = request.form.get("uname")
        password = encoder(request.form.get("psw"))
        if user in df.User.values:
            flash(f'Username {user} is already took')
            return redirect(url_for('register'))
        else:
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1}, ignore_index=True)
            df.to_csv('user.csv', index=False)
            return redirect(url_for('front'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)