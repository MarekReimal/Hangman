from _datetime import datetime
import glob
import sqlite3

from Leaderboard import Leaderboard


class Model:


    def __init__(self):
        self.database_name = 'databases/hangman_words_ee.db'  #  kui edit configuration parameters on teine fail kirjas siis võetakse see
        self.image_files = glob.glob('images/*.png')  # Loeb pildifailid listina mällu
        # New game
        self.new_word = None  # juhuslik sõna andmebaasist
        self.user_word = []  # kasutaja poolt leitud tähed ja kriipsud
        self.all_right_user_shars = []  # kõik õiged tähed
        self.all_wrong_user_chars = []  # kõik valesti sisestatud tähed
        self.all_user_chars = []  # valesti sisestatud tähed ühekordselt
        self.counter = 0  # Loendab valesid tähti
        # Leaderboard
        self.player_name = 'UNKNOWN'
        self.leaderboard_file = 'leaderboard.txt'
        self.score_data = []  # Leaderboard content data

    # arvuti peab võtma failist suvalise sõna ja näitama triibukesi
    def start_new_game(self):
        self.get_random_word()  #kutsub funks get_random_word
        #print(self.new_word)  # test prindib sõna konsooli
        self.user_word = []
        self.all_user_chars = []
        self.all_right_user_shars = []  # kõik õiged tähed
        self.all_wrong_user_chars = []  # kõik valesti sisestatud tähed
        self.counter = 0
        # kriipsude loomine sõna asemele
        for x in range(len(self.new_word)):  # loendab sõnas tähti
            self.user_word.append('_')  # Asendab kriipsudega

        print(self.new_word)  # Test nätab sõna
        # print(self.user_word)  # Test näitab sõna asemel kriipse

    #andmebaasiga ühenduse tekitamine
    def get_random_word(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.execute('SELECT * FROM words ORDER BY RANDOM() LIMIT 1')  #sorteeritakse juhuslikult ja võetakse üks rida
        self.new_word = cursor.fetchone()[1]  # 0=id 1=sõna, cursor sisaldab listi, fetchone- võtab ühe kirje, on ka fetchall
        connection.close()  # sulgeb ühenuse andmebaasiga

    def get_user_input(self, userinput): # sisendiks kasutaja poolt sisestatud täht
        # print(userinput, "  userinput*1*")
        if userinput: # kui täht on siis
            # print(userinput, "  userinput*2*")
            user_char = userinput[:1]  # ainult esimene täht
            # kast täht sõnas on olemas?
            if user_char.lower() in self.new_word.lower():
                if user_char.lower() in self.all_right_user_shars:  # kui täht on õigete tähtede listis
                    self.counter += 1  # siis suurendab vigade arvu
                else:  # kui täht puudub õigete listis siis
                    self.change_user_input(user_char)  # meetod ↓
                self.all_right_user_shars.append(user_char.lower())  # lisab kõik õiged tähed listi
            else:  # kui tähte ei ole sõnas
                self.counter += 1
                self.all_wrong_user_chars.append(user_char.lower()) # lisab kõik valed tähed listi
                # vormindab valede tähetede loetelu, 3xC,X,F
                self.all_user_chars = []  # list tühjaks
                except_from_count = []  # list tühjaks
                for t in self.all_wrong_user_chars:  # loendab valesid tähti
                    if t not in except_from_count:  # kontroll kas tähte juba loeti, välistab topelt kirjutamise
                        multi = self.all_wrong_user_chars.count(t)  # mitu korda tähte on listis
                        if multi > 1:  # kui tähte rohkem kui 1
                            my_str = str(multi) + 'x' + t.upper()  # vormindab väljundi korduvale tähele 3xZ
                            # listi all_user_chars SISU läheb ekraanile
                            self.all_user_chars.append(my_str)  # lisab listi korduva tähe 3xZ
                        else:
                            self.all_user_chars.append(t.upper())  # lisab listi üksiku tähe C
                    except_from_count.append(t)  # lisab listi tähe mis juba loetud
                    #print(except_from_count, "except_from_count")



    def change_user_input(self, user_char):
        # Asenda _ leitud tähega
        current_word = self.chars_to_list(self.new_word)  # sõna on vaja listina mitte stringina
        x = 0
        for c in current_word:
            if user_char.lower() == c.lower():  # kas täht on olemas
                self.user_word[x] = user_char.upper()  # asendab listis kriipsu suure tähega
            x += 1

    @staticmethod
    def chars_to_list(string):  # teeb stringi listiks
        # string to list test ['t', 'e', 's', 't']
        chars = []
        chars[:0] = string # viilutab
        return chars

    def get_all_user_chars(self):  # on list aga tahem et oleks string iga tähe jätrgi oleks koma ja tühik
        return ', '.join(self.all_user_chars)

    def set_player_name(self, name, seconds):  # küsib kasutajalt nime
        line = []  # siia lisatakse
        now = datetime.now().strftime('%Y-%m-%d %T')  # %T on sama mis kella aeg %H:%M:%S
        if name is not None: # .strip():  # kas kastaja on nime sisestanud, kui vajutatakse cancel siis viga ei teavita is not None
                                # None on siis kui vajutatakse cancel
            self.player_name = name.strip()

        line.append(now)  # aeg
        line.append(self.player_name)  # mängija nimi
        line.append(self.new_word)  # sõna
        line.append(self.get_all_user_chars())  # kõik valed tähed
        line.append(str(seconds))  # aeg sekundites
        # avab teksti faili, a+ teeb ka faili kui vaja
        with open(self.leaderboard_file, 'a+', encoding='utf-8') as f:
            f.write(';'.join(line) + '\n')

    def read_leaderboard_file_contents(self):
        # loeb faili sisu edetabelisse
        self.score_data = []
        empty_list = []
        all_lines = open(self.leaderboard_file, 'r', encoding='utf-8').readlines()
        # kõik read läbi käia ja iga rida teha objektiks
        for line in all_lines:
            parts = line.strip().split(';')
            empty_list.append((Leaderboard(parts[0], parts[1], parts[2], parts[3], int(parts[4]))))  # parts4 on aeg ja peab olema int
        self.score_data = sorted(empty_list, key=lambda x: x.time, reverse=False)  # sorteerib aja järgi, mis aeg on kõige lühem
        # x.time võib asendada ka indeksiga mitmenda järgi sorteerida tahad

        return self.score_data # tagastab kontrollerisse