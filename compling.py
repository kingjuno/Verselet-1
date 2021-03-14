import requests
from ExtraStuff2 import *
def compiler(code,lang):
    in1=code
    stdin = 'hi'

    stdin = 'hi'

    url = "https://rextester.com/rundotnet/api"
    to_compile = {
        "LanguageChoice": getid(lang),
        "Program": code,
        "Input": '',
        "CompilerArgs": ""
    }
    output = requests.post(url, data=to_compile)
    output = output.json()
    return output['Result'],output['Errors']