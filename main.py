import os.path

from Controller import Controller
from sys import argv  # käsurea lugemiseks


class Hangman:

    def __init__(self):
        Controller(db_name).main()  # andmebaasi nimi kaasa käsurealt ↓
        # loob controller() objekti
        # käivitab controlleri meetodi main()


if __name__ == '__main__':
    # print ("File1 __name__ = ", __name__)

    #vaja kontrollida kas käsurealt on db nimi antud
    # kui on kaks elementi antud, siis midagi on käsurealt siesestatud
    if len(argv) == 2:
        # vaja kontrollida kas selline fail ka on, sest kasutaja võis kirjutada suvalise nime
        if os.path.exists(argv[1]):
            db_name = argv[1]  # võetakse db nimi, kui nimi olemas
    Hangman()


# kodu töö
# kui täht algselt õige täht sisestatakse teist korda, siis see loetakse veaks ja listakse valesti arvatud tähtede hulka
# get_user_input juures
# alate kui objekt luuakse siis kohe tehaks init osa
# init on vaikimise vääärtused

# loe commandlinelt andmebaasi nimi
# module on def andmebaasi nimi

# enterklahvi tööle saamine muudatused > wiew konstruktor

# kontroll kas edetabeli fail on, alustades uues kohas mängu ei pruugi faili olemas olla > controller def click_btn_leaderboard(self)