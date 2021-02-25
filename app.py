from flask import Flask, render_template, request

app = Flask(__name__)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


users = []
users.append(User(id=1, username='arsh', password='pass'))
users.append(User(id=2, username='john', password='pass2'))


@app.route('/')
def front():
    return render_template('front.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
