import requests


def error(key):
    for i in key:
        if i[-5:]=='Error':
            return i 
        
gfg_compiler_api_endpoint = "https://ide.geeksforgeeks.org/main.php"
languages = ['C', 'Cpp', 'Cpp14', 'Java', 'Python', 'Python3', 'Scala', 'Php', 'Perl', 'Csharp']


def compiler(code, lang, _input=None, save=False):
    data = {
      'lang': lang,
      'code': code,
      'input': _input,
      'save': save
    }
    r = requests.post(gfg_compiler_api_endpoint, data=data)
    try:
        output_json = requests.post("https://ide.geeksforgeeks.org/submissionResult.php",data={"sid":r.json()["sid"],"requestType":"fetchResults"})
        while(output_json.json()['status']== 'IN-QUEUE'):
            output_json = requests.post("https://ide.geeksforgeeks.org/submissionResult.php",data={"sid":r.json()["sid"],"requestType":"fetchResults"})
        try:
            return str(output_json.json()['output']),None
        except:
            return None, str(output_json.json()[error([key for key in output_json.json().keys()])])
    except: 
        return None, str('Internal Server Error.')
