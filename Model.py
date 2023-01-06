import glob


class Model:

    def __init__(self):
        self.database_name = 'databases/hangman_words_ee.db'  #
        self.image_files = glob.glob('images/*.png')  # Loeb pildifailid listina mällu
        # New game
        self.new_word = None  # juhuslik sõna andmebaasist
        self.user_Word = []  # kasutaja poolt leitud tähed
        self.all_user_chars = []  # valesti sisestatud tähed
        self.counter = 0  # Loendab valesid tähti
        # Leaderboard
        self.player_name = 'UNKNOWN'
        self.leaderboard_file = 'leaderboard.txt'
        self.score_data = []  # Leaderboard content data