# Good luck team !!

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <style>
        h1 {
      background-color: #d5f4e6;
    }
    </style>
    <font face = "Lucida Calligraphy" size =" 5" color="orange"><b><h1 align="center">Hello SyntaEXE Team</h1><b></font>'''


if __name__ == '__main__':
    app.run(debug=True)
