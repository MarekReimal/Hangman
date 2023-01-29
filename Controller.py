from tkinter import simpledialog
from GameTime import GameTime
from Model import Model
from View import View


class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View(self, self.model) # kaasa controller ja model
        self.gametime = GameTime(self.view.lbl_time)  # label kaasa mille peal aega näidatakse


    def main(self):
        self.view.main()

    def click_btn_end(self):
        pass

    # kui vajutatakse uue mängu nupule
    # mis nupud lähevad peitu ja mis tulevad välja
    # pilt muudetakse tühjaks
    def click_btn_new(self):
        self.view.btn_new['state'] = 'disable'
        self.view.btn_cancel['state'] = 'normal'
        self.view.btn_send['state'] = 'normal'
        self.view.char_input['state'] = 'normal'
        self.view.change_image(0)  # muudab pildi indeksiga
        self.model.start_new_game()  # Alustab uut mängu
        self.view.lbl_result.configure(text=self.model.user_word)  # näitab kriipsudega sõna
        self.view.lbl_error.configure(text='Wrong 0 letter(s)', fg='black')  #  Teksti värv mustaks tagasi
        self.view.char_input.focus()
        self.gametime.reset()  # resetib aja
        self.gametime.start()  # alustab aja lugemist


    # mängu katkestamine
    def click_btn_cancel(self):
        self.gametime.stop()
        self.view.btn_new['state'] = 'normal'
        self.view.btn_cancel['state'] = 'disable'
        self.view.btn_send['state'] = 'disable'
        self.view.char_input['state'] = 'disable'
        self.view.char_input.delete(0, 'end')
        # muudab pildi ja näitab viimast
        self.view.change_image(len(self.model.image_files)-1)

    def click_btn_send(self):  # mida kasutaja on sisestanud, siin kutsub välja, toimetab mudelis
        self.model.get_user_input(self.view.userinput.get().strip())  #võtab vormilt info ja alguset ja lõpust võtab tühikud ära. get on vaja et info võtta
        self.view.lbl_result.configure(text=self.model.user_word)  # muudab labelil olevat osa
        self.view.lbl_error.configure(text=f'Wrong {self.model.counter} letters. {self.model.get_all_user_chars()} ')
        # kasutaja sisestus tuleb tühaks teha
        self.view.char_input.delete(0, 'end')  # kustutab esimesest kuni lõpuni
        if self.model.counter > 0:
            self.view.lbl_error.configure(fg='red')  # tähe värv
            self.view.change_image(self.model.counter)  # counter ütleb mitmes pilt võtta
        self.is_game_over()

    def is_game_over(self):  # alg seis taastatakse
        if self.model.counter >= 11 or '_' not in self.model.user_word or self.model.counter >= (len(self.model.image_files)-1): #counter loendab pilte, pilte on 11, kui viimane pilt on, siis järelikult on mäng läbi
            self.gametime.stop()  # aeg seisma
            self.view.btn_new['state'] = 'normal'
            self.view.btn_cancel['state'] = 'disable'
            self.view.btn_send['state'] = 'disable'
            self.view.char_input['state'] = 'disable'
            # küsi kasutaja nime
            player_name = simpledialog.askstring('Game over', 'What is the player\'s name', parent=self.view)  # askstring on valmis box küsimiseks
            # askstring vajab argumente päise info, info kasutajale
            self.model.set_player_name(player_name, self.gametime.counter)
            self.view.change_image(len(self.model.image_files)-1)

    def click_btn_leaderboard(self):
        # tekita aken
        popup_window = self.view.create_popup_window()
        data = self.model.read_leaderboard_file_contents()
        self.view.generate_leaderboard(popup_window, data)
