import string
c=['HMYS', 'M0MB', 'Q7A0', 'NBPG', '6J8G', 'SL6H', 'P03V', '4KBL', 'UBYU', 'UC5V', 'PNOH', 'M6G7', '2Z0N', '6XN8', 'GQ7X', 'JHUW', '63JP', 'OKSB', 'W0H0', 'UYOU', 'DWCV', 'CAJA', 'F6OJ', '5R1Y', '4YMC', 'BCNF', 'M1OJ', 'FY3Q', 'XWD0', 'L6XA', 'D9PR', 'A4A7', 'XDHL', 'IRP4', 'AXOP', 'B3EZ', 'T77V', '1TPC', 'BDQN', 'MCL8', 'EYDT', 'K6H6', 'GBQN', 'G6CK', 'NLTZ', 'QPRY', '2BHJ', '2X6W', '1MVK', 'YV8K', '1EEE', 'MMUR', '8MSC', 'NL35', 'CCDL', '3AUK', 'N0FL', 'EZE1', 'Z9W3', 'LVTO', 'TPMQ', 'LXQO', 'UPT5', 'TXVT', 'LR2A', 'XBBQ', 'RDEB', 'V3QH' ,'WHRG', 'FN3J', '7AIF', 'AFCU', 'OF65','MI7R', 'C3QJ', 'TRY0', 'E6Q8', '9JOS', 'F9T6', 'KPXY', 'Q3NJ', 'XVZV', 'PN0P', 'KLHD', 'ZACI', 'N57L', 'Y33G', 'QX0O','61ND','BIM3', 'QIIQ','JPOS','CZQQ']
b = string.ascii_letters+''.join(['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|',':',';','"',"'",'<',',','>','.','?','/','0','1','2','3','4','5','6','7','8','9'])


def encoder(x):
    a = ''
    for i in x.replace(' ', ''):
        a += f'{c[b.index(i)]} '
    return a


def decoder(encoded):
    d=''
    for i in encoded.split(' ')[:-1]:
        d += b[c.index(i)]
    return d