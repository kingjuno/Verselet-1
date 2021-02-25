from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd

app = Flask(__name__)
# u need a much stronger secret key so here it is
app.secret_key = 'ec52e5ead3899e4a0717b9806e1125de8af3bad84ca7f511'

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/')
def front():
    if 'user' in session:
        return render_template('front.html', name=session['user'])
    else:
        return render_template('front.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")
        if df[df['User'] == user]['Pass'].values == password:
            flash(f'you are logged in {user}')
            session['user'] = user
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
        password = request.form.get("psw")
        if user in df.User.values:
            flash(f'Username {user} is already taken')
            return redirect(url_for('register'))
        else:
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1}, ignore_index=True)
            df.to_csv('user.csv', index=False)
            return redirect(url_for('front'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)