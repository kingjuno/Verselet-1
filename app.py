from logging import debug
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import solution
import pandas as pd
from PIL import Image
from ExtraStuff import resize, hashpass
from Models import Room, db, init_room, update_room, delete_room, get_room
from websockets import socketio, send, emit, join_room, leave_room
import json
import os
import string
import random
from compling import *
q = 0
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio.init_app(app)
db.init_app(app)
UPLOAD_FOLDER = "static/pfps/"
login_manager = LoginManager()
app.secret_key = 'ec52e5ead3899e4a0717b9806e1125de8af3bad84ca7f511'
login_manager.init_app(app)
room_links = []


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
    db.init_app(app)
    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
@app.route('/', methods=['GET', 'POST'])
def front():
    global q, in_code,Question
    if 'user' in session:
        if request.method == "POST":
            if request.form['x'] == 'create':
                link = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
                room_links.append([link])

                df = pd.read_csv('questions.csv')
                Question=df['Questions'][random.randint(0,df.index[-1])]

                for i in room_links:
                    if i == link:
                        room_links.remove(link)
                        link = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
                        room_links.append([link])

                return redirect(f"/play/{link}")
            elif request.form['x'] == 'search':
                return redirect(f"play/{request.form.get('join')}")
        return render_template('homepage.html')

    else: return render_template('front.html')



@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        df = pd.read_csv('User.csv')
        user = request.form.get("uname")
        password = request.form.get("psw")
        print(df[df['User'] == user]['Pass'].values[0] == hashpass(password))
        session['user'] = user
        try:
            if df[df['User'] == user]['Pass'].values[0] == hashpass(password):
                session['user'] = user
                return redirect(url_for('front'))
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
            df = df.append({'User': user, 'Pass': password, 'Email': email, 'Id': len(df) + 1, 'DOB': dob},
                           ignore_index=True)
            df2 = df2.append({'Wins': 0, 'Games': 0, 'Avr. Time': 0, 'Username': user}, ignore_index=True)
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
    #try:
    dob = ''; e_mail = ''; inx = 0
    month = ['empty', 'January', 'F"ser"]}.png']
    udb = pd.read_csv('User.csv')
    df2=pd.read_csv('db.csv')
    wins = df2[df2['Username'] == session['user']]['Wins'].values[0]
    games = df2[df2['Username'] == session['user']]['Games'].values[0]
    for i in udb['User']:
        if udb['User'].values[inx] == session['user']:
            e_mail = udb['Email'][inx]; dob = udb['DOB'][inx]
        else: inx += 1
    pfp = f'static\pfps\{session["user"]}'
    # 2021-03-03

    doby = dob[0:4]
    if dob[5] == '0':
        dobm = month[int(dob[6])]
    else: dobm = month[int(dob[5:6])]
    if dob[8] == '0':
        dobd = dob[9]
    else: dobd = dob[8:9]

    return render_template('profile.html', w=wins, pfp=pfp, g=games, u=session['user'], e=e_mail, d=dobd, m=dobm, y=doby)
    #except:
     #   flash("Please login or create an account first")
      #  return redirect(url_for('login'))

@app.route('/code', methods=['GET', 'POST'])
def code():
    if request.method == "POST":
        in_code = request.form.get('input')
        lang = request.form.get('lang')
        result, errors = compiler(in_code, lang)
        result = result.replace("\n", '\n')
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
                        uploaded_file = request.files["file"]
                        if request.form.get('unameedit') != "" or request.form.get(
                                'emailedit') != "" or request.form.get('dob') != "" or request.form.get(
                                'passedit') != "" or uploaded_file.filename != "":
                            # CHECK IF PASSWORD IS CORRECT
                            if hashpass(request.form.get('p')) == df.Pass[inx]:
                                print('password is correct')
                                index = 0
                                # USERNAME EDIT
                                if request.form.get('unameedit') != "":
                                    print('username is filled')
                                    if request.form.get('unameedit') in list(df.User):
                                        flash("Username already taken")
                                        settings_page()
                                        return render_template('settingspage.html')
                                    else:
                                        df.replace(to_replace=df.User[inx], value=request.form.get('unameedit'),
                                                   inplace=True)
                                        df.to_csv('User.csv', index=False)
                                        print('replaced username in db')
                                        for j in ud.Username:
                                            if j == session['user']:
                                                ud.replace(to_replace=ud.Username[inx],
                                                           value=request.form.get('unameedit'),
                                                           inplace=True)
                                                ud.to_csv('db.csv', index=False)
                                                print('replaced username in user_db')
                                                os.rename('static/pfps/' + session['user'] + '.png',
                                                          'static/pfps/' + request.form.get('unameedit') + '.png')
                                                print('changed pfp name')
                                                session['user'] = request.form.get('unameedit')
                                                print('session user set')
                                            else:
                                                index += 1
                                # EMAIL EDIT
                                if request.form.get('emailedit') != "":
                                    print('email is filled')
                                    if request.form.get('emailedit') in list(df.Email):
                                        flash("An account with this email address already exists")
                                        settings_page()
                                        return render_template('settingspage.html')
                                    else:
                                        df.replace(to_replace=df.Email[inx], value=request.form.get('emailedit'),
                                                   inplace=True)
                                        df.to_csv('User.csv', index=False)
                                        print('email is replaced')
                                # PROFILE PICTURE EDIT
                                if uploaded_file.filename != "":
                                    os.remove(UPLOAD_FOLDER + session['user'] + '.png')
                                    uploaded_file.save(os.path.join(UPLOAD_FOLDER, i + '.png'))
                                    # Resize profile pic to 64x64
                                    resize(os.path.join(UPLOAD_FOLDER, i + '.png'))
                                # PASSWORD EDIT
                                if request.form.get('passedit') != "":
                                    print('password needs change')
                                    df.replace(to_replace=df.Pass[inx], value=hashpass(request.form.get('passedit')),
                                               inplace=True)
                                    df.to_csv('User.csv', index=False)
                                    print('changed pass')
                                return render_template('homepage.html')
                            else:
                                flash('Incorrect password')
                                return render_template('settingspage.html')
                    else:
                        inx += 1
                return render_template('homepage.html')
            return render_template('settingspage.html', w=wins, g=games, u=session['user'], e=e_mail, d=dob)
        except Exception:
            return render_template('login.html')
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

                    print('sent')
                    return redirect(url_for('front'))

                else:
                    index += 1

        return render_template('contact.html')
    else:
        flash('Please login first.')
        return redirect('/login')


@app.route('/play', methods=['GET', 'POST'])
def play():

    if 'user' in session:
        return render_template('play.html', u=session['user'])
    else:
        flash("Please log in")
        return redirect(url_for('login'))





@app.route(f'/play/<roomlink>', methods=['GET', 'POST'])
def room(roomlink):
    global in_code,Question
    if 'user' in session:
        index = 0
        df = pd.read_csv('questions.csv')
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
                    if request.form['btnc'] == 'run':

                        qinx = 0
                        for qw in df['Questions']:
                            if qw == room_links[index][1]:
                                if df['type'][qinx]=='code':
                                    print(df['Answers'][qinx])
                                    b=[]
                                    input1=(df['Inputs'][qinx])
                                    exec(df['Answers'][qinx])
                                    q_answer='\n'+'\n'.join(b)
                                    print(q_answer)
                                else:
                                    q_answer = df['Answers'][qinx]

                                break
                            else: qinx += 1

                        in_code = request.form.get('input')
                        lang = request.form.get('lang')
                        result, errors = compiler(in_code, lang, df['Inputs'][qinx])
                        result = result
                        q_answer = q_answer
                        print(q_answer, result)
                        a=[]
                        if result and len(result)==len(q_answer):
                            answer=q_answer.replace('\n','')
                            r=result.replace('\n','')
                            for z in range(len(answer)):
                                if not answer[z] == r[z]:
                                    a.append('Nope, this one is wrong too')
                        else:
                            a.append('No chance of this being correct')
                        if errors is not None:
                            return render_template('compiler.html', e=errors, c=in_code, que=room_links[index][1], link=roomlink, q=f'Result : {result == q_answer}' if result else '')
                        else:
                            return render_template('compiler.html', r=result, c=in_code, q=f'Result : True' if not a else 'Result : False', que=room_links[index][1], link=roomlink, z=f"Expected : {q_answer}")
                    elif request.form['btnc'] == 'submit':
                        a = []
                        if a:
                            answer="Wrong"
                        else:
                            answer="Correct"
                        name_v = session['user']
                        status = "done"
                        code = "nothing"
                        init_room(roomlink,status,name_v,code)
                        room = get_room(roomlink)
                        username = room['names']
                        status = room['status']
                        indexs = 0
                        for index in room['names']:
                            indexs+=1
                        return render_template('result.html', username=username,status=status,answer=answer,index=indexs)


                return render_template('compiler.html', u=session['user'], que=room_links[index][1], link=roomlink,c=in_code)
            else:
                index += 1
        else:
            return render_template('404.html')
    else:solution

""" @app.route("/testdb", methods=["GET","POST"])
def testdb():
    if request.method == "POST":
        init_room("123","some status","emil test 123", "some code")
        update_room("123",code="some other code")
        print(get_room("123"))
    if request.method == "GET":
        print(get_room("123"))
        delete_room("123")
        print(get_room("123")) """

if __name__ == '__main__':
    socketio.run(app ,debug=True)

## @Nuke Ninja 
# call init_room(roomlink, status,names,code) when the room is created and delete(roomlink) when you delete it.
# call update_room(roomlink, whatever you want to change) and get_room(roomlink) to get all the values as a dict. 