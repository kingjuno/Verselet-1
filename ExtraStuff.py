from PIL import Image 

def hash(password:str):
    # imports
    import hashlib
    import base64
    # encrypting
    a = hashlib.sha256()
    a.update(bytes(password.encode()))
    b = []
    b.append(str(a.digest()).split("'")[1])
    b[0] = str(base64.urlsafe_b64encode(bytes(b[0].encode()))).split("'")[1]
    # salting
    salt = ['$', '#', '!', '~', '@', '^', '&', '`', '%', '*', '_', '-', '.', '|', ':', ';', '?']
    c = (b[0].split("G"))
    d = []
    e = []
    for i in range(len(c)):
        a = salt[i]
        b = c[i]
        c[i] = b+a
    for i in range(len(c)):
        try:
            d.append(c[i+1])
        except:
            d.append(c[0])
    e.append(''.join(d))
    return(e[0])

def resize(path):
    im = Image.open(path)
    im= im.resize((64,64))
    im.save(path)  
