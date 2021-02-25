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
    h2 {
      background-color: #d5f4e6;
    }
    </style>
    <font face = "Arial" size =" 5" color="black"><b><h1 align="center">Hello SyntaEXE Team !</h1><b></font>
    <font face = "Arial" color="black"><h2>Good luck team and remember, the members in the server are always ready to help !</h2></font>
    '''


if __name__ == '__main__':
    app.run(debug=True)
