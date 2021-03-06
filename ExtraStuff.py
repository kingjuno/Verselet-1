from PIL import Image 

def hashpass(password:str):
    import hashlib, base64
    a = hashlib.sha256(); a.update(bytes(password.encode())); b = []
    base = hashlib.sha512()
    md = hashlib.md5()
    b.append(str(a.digest()).split("'")[1])
    b[0] = str(base64.urlsafe_b64encode(bytes(b[0].encode()))).split("'")[1]
    base.update(bytes(b[0].encode()))
    md.update(base.digest())
    b[0]=str(base64.urlsafe_b64encode(base64.standard_b64encode(md.digest()))).split("'")[1]
    # salting
    salt = ['H', 'c', 'D', 'L', 'b', 'M', 'S', 'a', 'N', 'q', 'K', 'j', 'V', 'd', 'O', 'W', 'x']
    c = (b[0].split("G"or"g"or"v"or"x")); d = []; e = []

    for i in range(len(c)): a = salt[i]; b = c[i]; c[i] = b+a

    for i in range(len(c)):

        try: d.append(c[i+1])

        except: d.append(c[0])

    e.append(''.join(d))
    print(e[0])
    return(e[0])

def resize(path):
    im = Image.open(path)
    im = im.resize((64,64))
    im.save(path)  
