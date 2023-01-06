from Controller import Controller


class Hangman:

    def __init__(self):
        Controller().main()
        # loob controller() objekti
        # käivitab controlleri meetodi main()


if __name__ == '__main__':
    Hangman()