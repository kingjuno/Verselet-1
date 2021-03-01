from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user, UserMixin
import pandas as pd
from PIL import Image
from ExtraStuff import decoder, encoder
import os

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
    if 'user' in session: return render_template('homepage.html')
    else: return render_template('front.html')


@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        df = pd.read_csv('user.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")
        try:
            if decoder(df[df['User'] == user]['Pass'].values[0]) == password:
                session['user'] = user
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
            flash(f'An account with that username already exists.')
            return redirect(url_for('register'))
        elif email in df.Email.values:
            flash(f'An account with that email address already exists.')
            return redirect(url_for('register'))
        else:
            df2 = pd.read_csv('db.csv')
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1, 'DOB': dob},
                           ignore_index=True)
            df2 = df2.append({'Wins': 0, 'Games': 0, 'Avr. Time': 0, 'Username': user}, ignore_index=True)
            df2.to_csv('db.csv', index=False)
            df.to_csv('user.csv', index=False)
            session['user'] = user
            im1 = Image.open('static/base.png')
            im1.save(f'static/{user}.png')
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
        pfp = f'static/{session["user"]}.png'
        udb = pd.read_csv('User.csv')
        wins = df2[df2['Username'] == session['user']]['Wins'].values[0]
        games = df2[df2['Username'] == session['user']]['Games'].values[0]
        for i in udb['User']:
            if udb['User'].values[inx] == session['user']:
                e_mail = udb['Email'][inx]; dob = udb['DOB'][inx]
            else: inx += 1
        doby = dob[0:4]; dobd = dob[8:10]
        if '0' == dob[5]: dobm = month[int(dob[6])]
        else: dobm = month[int(dob[5:7])]
        return render_template('profile.html', w=wins, pfp=pfp, g=games, u=session['user'], e=e_mail, d=dobd, m=dobm, y=doby)
    except:
        flash("Please login or create an account first")
        return redirect(url_for('login'))


@login_manager.user_loader
@app.route('/settings', methods=['POST', 'GET'])
def settings_page():
    if 'user' in session:
        try:

            # PASSING ALL INFO TO DISPLAY

            dob = ''; e_mail = ''; inx = 0
            month = ['empty', 'January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            df2 = pd.read_csv('db.csv')
            udb = pd.read_csv('User.csv')
            wins = df2[df2['Username'] == session['user']]['Wins'].values[0]
            games = df2[df2['Username'] == session['user']]['Games'].values[0]
            for i in udb['User']:
                if udb['User'].values[inx] == session['user']: e_mail = udb['Email'][inx];dob = udb['DOB'][inx]
                else: inx += 1

            # DOING THE ACTUAL CHANGES

            if request.method == 'POST':
                df = pd.read_csv('User.csv'); ud = pd.read_csv('db.csv'); inx = 0
                for i in df.User:
                    if i == session['user']:
                        # CHECKING IF ANY CHANGES ARE REQUESTED
                        if request.form.get('unameedit') != " " or request.form.get(
                                'emailedit') != " " or request.form.get('dob') != " " or request.form.get(
                                'passedit') != " ":
                            # CHECK IF PASSWORD IS CORRECT
                            if request.form.get('p') == decoder(df.Pass[inx]):
                                index = 0
                                # USERNAME EDIT
                                if request.form.get('unameedit') != " ":
                                    print('ayyyyy')
                                    if request.form.get('unameedit') in list(df.User):
                                        print('failed')
                                        flash("Username already taken")
                                        print('returning to page')
                                        return render_template('settingspage.html')
                                    else:
                                        df.replace(to_replace=df.User[inx], value=request.form.get('unameedit'),
                                                   inplace=True)
                                        df.to_csv('User.csv', index=False)
                                        for j in ud.Username:
                                            if j == session['user']:
                                                ud.replace(to_replace=ud.Username[inx],
                                                           value=request.form.get('unameedit'),
                                                           inplace=True)
                                                ud.to_csv('db.csv', index=False)
                                                os.rename('static/' + session['user'] + '.png',
                                                          'static/' + request.form.get('unameedit') + '.png')
                                                session['user'] = request.form.get('unameedit')
                                            else:
                                                index += 1
                                # EMAIL EDIT
                                if request.form.get('emailedit') != " " and request.form.get('emailedit') not in df.Email:
                                    df.replace(to_replace=df.Email[inx], value=request.form.get('emailedit'),
                                               inplace=True)
                                    df.to_csv('User.csv', index=False)
                                # PASSWORD EDIT
                                if request.form.get('passedit') != " ":
                                    df.replace(to_replace=df.Pass[inx], value=encoder(request.form.get('passedit')),
                                               inplace=True)
                                    df.to_csv('User.csv', index=False)
                                return render_template('homepage.html')
                            else:
                                flash('Incorrect password.')
                                settings_page()
                    else: inx += 1
                return render_template('homepage.html')
            return render_template('settingspage.html', w=wins, g=games, u=session['user'], e=e_mail, d=dob)
        except:
            login()
            return render_template('login.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
