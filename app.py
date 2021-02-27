from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user, UserMixin
import pandas as pd
from ExtraStuff import decoder, encoder

app = Flask(__name__)

login_manager = LoginManager()
app.secret_key = 'ec52e5ead3899e4a0717b9806e1125de8af3bad84ca7f511'
login_manager.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
@app.route('/')
def front():
    if 'user' in session:
        return render_template('homepage.html')
    else:
        return render_template('front.html')


@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")

        try:
            if df[df['User'] == user]['Pass'].values[0] == encoder(password):
                session['user'] = user
                flash(f'Welcome, {user}')
                return redirect(url_for('user_profile'))
            else:
                flash('Incorrect username or password')
                redirect(url_for('login'))

        except:
            flash('Incorrect username or password')
            redirect(url_for('login'))
    return render_template('login.html')


@login_manager.user_loader
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        email = request.form.get('email')
        user = request.form.get("uname")
        password = encoder(request.form.get("psw"))
        dob = request.form.get('dob')
        if user in df.User.values:
            flash(f'Username {user} is already taken')
            return redirect(url_for('register'))
        else:
            df2 = pd.read_csv('db.csv')
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1, 'DOB': dob},
                           ignore_index=True)
            df2 = df2.append({'Wins': 0, 'Games': 0, 'Avr. Time': 0, 'Username': user}, ignore_index=True)
            df2.to_csv('db.csv', index=False)
            df.to_csv('user.csv', index=False)
            return redirect(url_for('front'))
    return render_template('register.html')


@login_manager.user_loader
@app.route('/profile')
def user_profile():
    try:
        dob = ''; e_mail = ''; inx = 0
        month = ['empty', 'January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        df2 = pd.read_csv('db.csv')
        udb = pd.read_csv('User.csv')
        wins = df2[df2['Username'] == session['user']]['Wins'].values[0]
        games = df2[df2['Username'] == session['user']]['Games'].values[0]
        for i in udb['User']:
            if udb['User'].values[inx] == session['user']:
                e_mail = udb['Email'][inx]; dob = udb['DOB'][inx]
            else:
                inx += 1
        # 2007-01-02
        doby = dob[0:4]; dobd = dob[8:10]
        if '0' == dob[5]:
            dobm = month[int(dob[6])]
        else:
            dobm = month[int(dob[5:7])]
        return render_template('profile.html', w=wins, g=games, u=session['user'], e=e_mail, d=dobd, m=dobm, y=doby)
    except:
        flash("Please login or create an account first")
        return redirect(url_for('login'))


@login_manager.user_loader
@app.route('/settings')
def settings_page():
    if 'user' in session:
        return render_template('settingspage.html')
    else:
        login()
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
    print(session['user'])
