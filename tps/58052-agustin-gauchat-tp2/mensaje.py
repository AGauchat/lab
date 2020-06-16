from tobit import tobits
import os

def mensa(mensaj):
    mens = open(mensaj, "rb").read().decode()
    mensa = tobits(mens, '2')
    mens = ''.join([str(elem) for elem in mensa])
    sis = os.path.getsize(mensaj)
    return mens, sis