import string

b = string.ascii_letters+''.join(['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|',':',';','"',"'",'<',',','>','.','?','/','0','1','2','3','4','5','6','7','8','9'])


def encoder(x):
    a = ''
    for i in x.replace(' ',''):
        a += f'{b.index(i)} '
    return a


def decoder(encoded):
    d=''
    for i in encoded.split(' ')[:-1]:
        d+=b[int(i)]
    return d