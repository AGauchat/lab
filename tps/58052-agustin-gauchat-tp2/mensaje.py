from tobit import tobits
import os
from rot13 import rot13

def mensa(mensaj, rot13Val):
    if (rot13Val):
        mens = rot13(open(str(mensaj), "r").read())
    else:
        mens = open(str(mensaj), "r").read()
    # mens = open(str(mensaj), "rb").read().decode()
    mensa = tobits(mens, '2')
    mens = ''.join([str(elem) for elem in mensa])
    sis = os.path.getsize(mensaj)
    return mens, sis