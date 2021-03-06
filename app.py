from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from websockets import socketio, send, emit, join_room, leave_room, close_room
from email.mime.multipart import MIMEMultipart
from ExtraStuff import resize, hashpass
from email.mime.text import MIMEText
from flask_login import LoginManager
from compling import *
from PIL import Image
from Models import *
import threading
import pandas as pd
import smtplib
import random
import string
import ast
import os

q = 0
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio.init_app(app)
UPLOAD_FOLDER = "static/pfps/"
login_manager = LoginManager()
app.secret_key = 'ec52e5ead3899e4a0717b9806e1125de8af3bad84ca7f511'
login_manager.init_app(app)
room_links = []


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
@app.route('/', methods=['GET', 'POST'])
def front():
    global Question


    usdb = pd.read_csv('db.csv'); pi = 0; ee = ''; ei = 0; return_link = ''
    if 'user' in session:

        if request.method == "POST":
            usdb = pd.read_csv('db.csv'); pi = 0; usl = ''
            for i in usdb.username.values:
                if i == session['user']:
                    usl = usdb['current'][pi]
                    break
                else:
                    pi += 1

            if request.form['x'] == 'gamemain':
                if usl == 'Create a game':
                    link = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
                    room_links.append([link])

                    df = pd.read_csv('questions.csv')
                    Question = df['Questions'][random.randint(0, df.index[-1])]

                    for i in room_links:
                        if i == link:
                            room_links.remove(link)
                            link = ''.join(
                                random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
                            room_links.append([link])

                    for i in usdb.username.values:
                        if i == session['user']:
                            usdb.loc[usdb["username"] == session['user'], "games"] += 1
                            usdb.loc[usdb["username"] == session['user'], "current"] = 'Rejoin your game'
                            usdb.loc[usdb["username"] == session['user'], "link"] = link
                            usdb.to_csv('db.csv', index=False)
                            break

                    init_room(link, 'on_going', session['user'], [session['user']])
                    return redirect(f"/play/{link}")
                else:
                    for i in usdb.username.values:
                        if i == session['user']:
                            return_link = usdb['link'][ei]
                            break
                        else:
                            ei += 1

                    return redirect(f"play/{return_link}")

            elif request.form['x'] == 'search':
                search_link = request.form.get('join'); dbroom = pd.read_csv('rooms.csv'); usdb = pd.read_csv('db.csv'); roomi = 0
                if usl == 'Create a game':
                    for i in dbroom['link']:
                        if i == search_link:
                            if roomi < len(dbroom['link']):
                                usern = dbroom.n[roomi]
                                userl = ast.literal_eval(usern)
                                if session['user'] in userl:
                                    break
                                else:
                                    for i in usdb.username.values:
                                        if i == session['user']:
                                            usdb.loc[usdb["username"] == session['user'], "games"] += 1
                                            usdb.loc[usdb["username"] == session['user'], "current"] = 'Rejoin your game'
                                            usdb.loc[usdb["username"] == session['user'], "link"] = request.form.get('join')
                                            usdb.to_csv('db.csv', index=False)
                                            break
                                    userl.append(session['user'])
                                dbroom.replace(to_replace=dbroom.n[roomi], value=str(userl), inplace=True)
                                dbroom.to_csv('rooms.csv', index=False)
                                break
                            else:
                                break
                    else:
                        roomi += 1
                    return redirect(f"play/{request.form.get('join')}")
                else:
                    flash('You are already in a game')
                    return render_template('homepage.html', b=usl)

            elif request.form['x'] == 'rejoin':
                return redirect(f"play/{usl}")

        for i in usdb.username.values:
            if i == session['user']:
                ee = usdb['current'][pi]
                break
            else:
                pi += 1

        return render_template('homepage.html', b=ee)
    else:
        return render_template('front.html')

@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        df = pd.read_csv('User.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")
        try:
            log_inx = 0
            for i in df['User']:
                if i == user:
                    if hashpass(password) == df['Pass'][log_inx]:
                        session['user'] = user
                        return redirect(url_for('front'))
                else:
                    log_inx += 1
            else:
                flash('Incorrect username or password')
                return render_template("login.html")
        except:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    return render_template('login.html')



@login_manager.user_loader
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        df = pd.read_csv('User.csv')
        email = request.form.get('email')
        user = request.form.get("uname")
        password = hashpass(request.form.get("psw"))
        dob = request.form.get('dob')
        if user in df.User.values:
            flash(f'An account with that username already exists.')
            return redirect(url_for('register'))
        elif email in df.Email.values:
            flash(f'An account with that email address already exists.')
            return redirect(url_for('register'))
        else:
            df2 = pd.read_csv('db.csv')
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1, 'DOB': dob}, ignore_index=True)
            df2 = df2.append({'wins': 0, 'games': 0, 'time': 0, 'username': user, 'current': '0'}, ignore_index=True)
            df2.to_csv('db.csv', index=False)
            df.to_csv('User.csv', index=False)
            session['user'] = user
            im1 = Image.open('static/pfps/base.png')
            im1.save(f'static/pfps/{user}.png')
            return redirect(url_for('front'))
    return render_template('register.html')


@login_manager.user_loader
@app.route('/profile')
def user_profile():
    if 'user' in session:
        dob = ''; e_mail = ''; inx = 0
        month = ['empty', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        udb = pd.read_csv('User.csv')
        df2 = pd.read_csv('db.csv')
        wins = df2[df2['username'] == session['user']]['wins'].values[0]
        games = df2[df2['username'] == session['user']]['games'].values[0]
        for i in udb['User']:
            if udb['User'].values[inx] == session['user']:
                e_mail = udb['Email'][inx]; dob = udb['DOB'][inx]
            else: inx += 1
        pfp = f'static\pfps\{session["user"]}.png'

        doby = dob[0:4]
        if dob[5] == '0':
            dobm = month[int(dob[6])]
        else:
            dobm = month[int(dob[5:6])]
        if dob[8] == '0':
            dobd = dob[9]
        else:
            dobd = dob[8:9]

        return render_template('profile.html', w=wins, pfp=pfp, g=games, u=session['user'], e=e_mail, d=dobd, m=dobm, y=doby)
    else:
        flash("Please login or create an account first")
        return redirect(url_for('login'))

@app.route('/code', methods=['GET', 'POST'])
def code():
    if request.method == "POST":
        in_code = request.form.get('input')
        lang = 'Python'
        result, errors = compiler(in_code, lang)
        # result = result.replace("\n", '\n')
    else:
        result = ''; in_code = ''; errors = ''
    if errors != None:
        return render_template('compiling.html', e=errors, c=in_code)
    elif errors == None and result != None :
        return render_template('compiling.html', r=result, c=in_code)
    return render_template('compiling.html')


@login_manager.user_loader
@app.route('/about', methods=['POST', 'GET'])
def aboutus():
    return render_template('about.html')


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
            wins = df2[df2['username'] == session['user']]['wins'].values[0]
            games = df2[df2['username'] == session['user']]['games'].values[0]
            for i in udb['User']:
                if udb['User'].values[inx] == session['user']: e_mail = udb['Email'][inx];dob = udb['DOB'][inx]
                else: inx += 1

            # DOING THE ACTUAL CHANGES

            if request.method == 'POST':

                df = pd.read_csv('User.csv'); ud = pd.read_csv('db.csv'); inx = 0
                for i in df.User:
                    if i == session['user']:
                        # CHECKING IF ANY CHANGES ARE REQUESTED
                        uploaded_file = request.files["file"]
                        if request.form.get('unameedit') != "" or request.form.get(
                                'emailedit') != "" or request.form.get('dob') != "" or request.form.get(
                                'passedit') != "" or uploaded_file.filename != "":
                            # CHECK IF PASSWORD IS CORRECT
                            if hashpass(request.form.get('p')) == df.Pass[inx]:
                                index = 0
                                # USERNAME EDIT
                                if request.form.get('unameedit') != "":
                                    if request.form.get('unameedit') in list(df.User):
                                        flash("Username already taken")
                                        settings_page()
                                        return render_template('settingspage.html')
                                    else:
                                        df.loc[df["User"] == session['user'], "User"] = request.form.get('unameedit')
                                        df.to_csv('User.csv', index=False)
                                        for j in ud.username:
                                            if j == session['user']:
                                                ud.loc[ud["username"] == session['user'], "username"] = request.form.get('unameedit')
                                                ud.to_csv('db.csv', index=False)
                                                os.rename('static/pfps/' + session['user'] + '.png',
                                                          'static/pfps/' + request.form.get('unameedit') + '.png')
                                                session['user'] = request.form.get('unameedit')
                                            else:
                                                index += 1
                                # EMAIL EDIT
                                if request.form.get('emailedit') != "":
                                    if request.form.get('emailedit') in list(df.Email):
                                        flash("An account with this email address already exists")
                                        settings_page()
                                        return render_template('settingspage.html')
                                    else:
                                        df.replace(to_replace=df.Email[inx], value=request.form.get('emailedit'),
                                                   inplace=True)
                                        df.to_csv('User.csv', index=False)
                                # PROFILE PICTURE EDIT
                                if uploaded_file.filename != "":
                                    os.remove(UPLOAD_FOLDER + session['user'] + '.png')
                                    uploaded_file.save(os.path.join(UPLOAD_FOLDER, i + '.png'))
                                    # Resize profile pic to 64x64
                                    resize(os.path.join(UPLOAD_FOLDER, i + '.png'))
                                # PASSWORD EDIT
                                if request.form.get('passedit') != "":
                                    df.replace(to_replace=df.Pass[inx], value=hashpass(request.form.get('passedit')),
                                               inplace=True)
                                    df.to_csv('User.csv', index=False)
                                return render_template('homepage.html')
                            else:
                                flash('Incorrect password')
                                return render_template('settingspage.html')
                    else:
                        inx += 1
                return front()

            return render_template('settingspage.html', w=wins, g=games, u=session['user'], e=e_mail, d=dob)
        except Exception:
            return redirect(url_for('login'))
    else:
        flash('Please login first.')
        return redirect(url_for('login'))


@login_manager.user_loader
@app.route('/contact', methods=['POST', 'GET'])
def contactus():
    if 'user' in session:
        if request.method == 'POST':
            df = pd.read_csv('User.csv'); index = 0
            for i in df.User:
                if i == session['user']:

                    from_add = 'syntaexe@gmail.com'
                    to_add = ['syntaexe@gmail.com']
                    msg = MIMEMultipart()
                    msg['From'] = from_add
                    msg['To'] = ' ,'.join(to_add)

                    msg['Subject'] = str(request.form.get('title'))
                    body = f'From: {str(request.form.get("name"))} ({str(df.Email[index])}), {str(request.form.get("body"))}'
                    msg.attach(MIMEText(body, 'plain'))

                    email = 'syntaexe@gmail.com'
                    password = 'syntaxexe'

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(email, password)
                    text = msg.as_string()
                    mail.sendmail(from_add, to_add, text)
                    mail.quit()

                    return redirect(url_for('front'))

                else:
                    index += 1

        return render_template('contact.html')
    else:
        flash('Please login first.')
        return redirect('/login')


@app.route(f'/play/<roomlink>', methods=['GET', 'POST'])
def room(roomlink):
    global in_code,Question, q_answer, userl, a
    if 'user' in session:
        index = 0; df = pd.read_csv('questions.csv'); udb = pd.read_csv('db.csv')
        for i in room_links:
            if i[0] == roomlink:

                room_links[index].append(Question); qindex = 0

                for qvar in df['Questions']:
                    if qvar == room_links[index][1]:
                        if df['type'][qindex] == 'int':
                            in_code = '''
x = input().split('$')
for i in x:
    i = int(i)

print('YOUR ANSWER')                                                    
'''
                        else:
                            in_code = '''
x = input().split('$')
for i in x:
    pass
    
print('YOUR ANSWER')                                                                                                                                                                                    
'''
                    else: qindex += 1

                if request.method == "POST":
                    is_correct = False
                    if request.form['btnc'] == 'run':

                        qinx = 0
                        for qw in df['Questions']:
                            if qw == room_links[index][1]:
                                if df['type'][qinx] == 'code':
                                    b = []
                                    input1 = (df['Inputs'][qinx])
                                    exec(df['Answers'][qinx])
                                    q_answer = '\n'+'\n'.join(b)
                                else:
                                    q_answer = df['Answers'][qinx]

                                break
                            else:
                                qinx += 1

                        in_code = request.form.get('input')
                        lang = 'Python3'
                        result, errors = compiler(in_code, lang, _input=df['Inputs'][qinx])
                        if result != None:
                            a = []
                            if len(result) == len(q_answer):
                                answer = q_answer
                                for z in range(int(len(answer))):
                                    if str(answer[z]) != str(result[z]):
                                        a.append('Nope, this one is wrong too')
                            else:
                                a.append('No chance of this being correct')
                        if errors is not None:
                            return render_template('compiler.html', e=errors, c=in_code, que=room_links[index][1], link=roomlink, q=f'Result : {result == q_answer}' if result else '')
                        else:
                            if a != []:
                                is_correct = False
                            else:
                                is_correct = True
                            return render_template('compiler.html', r=result, c=in_code, q=f'Result : True' if is_correct else 'Result : False', que=room_links[index][1], link=roomlink, z=f"Expected : {q_answer}")

                    elif request.form['btnc'] == 'submit':
                        udb.loc[udb["username"] == session['user'], "current"] = 'Create a game'
                        if is_correct:
                            answer = "Correct"
                        else:
                            answer = "Inorrect"

                        room = get_room(roomlink)
                        # [["link", room_link], ["status", room_status], ['name', room_name], ["n", room_names]]
                        userl = ast.literal_eval(room[3][1])
                        username = session['user']
                        status = room[1][1]
                        indexs = 0
                        for index in room[2]:
                            indexs += 1

                        return render_template('result.html', username=username, status=status, answer=answer, index=indexs, userlist=userl)

                    elif request.form['btnc'] == 'leave':
                        usdb = pd.read_csv('db.csv'); roomdb = pd.read_csv('rooms.csv'); roomi = 0

                        for i in roomdb.link.values:
                            if i == roomlink:
                                usern = roomdb.n[roomi]
                                userl = ast.literal_eval(usern)
                                userl.remove(str(session['user']))
                                roomdb.replace(to_replace=roomdb.n[roomi], value=str(userl), inplace=True)
                                roomdb.to_csv('rooms.csv', index=False)
                                if roomdb.n[roomi] == '[]':
                                    roomdb.drop(roomi, axis=0, inplace=True)
                                    roomdb.to_csv('rooms.csv', index=False)
                                    close_room(roomlink)
                            else:
                                roomi += 1

                        usdb.loc[usdb["username"] == session['user'], "current"] = 'Create a game'
                        usdb.loc[udb["username"] == session['user'], "link"] = ''

                        usdb.to_csv('db.csv', index=False)

                        return redirect(url_for('front'))

                return render_template('compiler.html', u=session['user'], que=room_links[index][1], link=roomlink, c=in_code)
            else:
                index += 1
        else:
            return render_template('404.html')
    else:
        pass

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
