from Controller import Controller


class Hangman:

    def __init__(self):
        Controller().main()
        # loob controller() objekti
        # käivitab controlleri meetodi main()


if __name__ == '__main__':
    Hangman()


# kodu töö
# kui täht algselt õige täht sisestatakse teist korda, siis see loetakse veaks ja listakse valesti arvatud tähtede hulka
# get_user_input juures
# alate kui objekt luuakse siis kohe tehaks init osa
# init on vaikimise vääärtused
