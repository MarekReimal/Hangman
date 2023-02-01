from datetime import datetime, timedelta
from tkinter import *
import tkinter.font as tkfont  # tkfont on alias
from tkinter import ttk

from PIL import Image, ImageTk # on vaja poomis piltide kasutamsieks, PIL vaja installida> vali alt+enter install Pil 2. rida

class View(Tk):

    def __init__(self, controller, model):
        super().__init__()  # super on Tk
        self.controller = controller
        self.model = model
        self.userinput = StringVar()

        # kirjastiilide defineerimine
        self.big_font_style = tkfont.Font(family='Courier', size=18, weight='bold')  # tkfont vaja importida
        self.default_style_bold = tkfont.Font(family='Verdana', size=10, weight='bold')  # tkfont vaja importida
        self.default_style = tkfont.Font(family='Verdana', size=10)  # tkfont vaja importida

        # Window properties
        self.geometry('515x200')
        self.title('Hangman TAK22')
        self.center(self)  # klassi sees olev meetod 'center'

        # create two frames  (teeme meetodi enne valmis all pool def create_two_frames)
        # töö põhimõte, all tehakse meetod, mis tagastav (väljastab) nupud, siin kutsutakse meetod välja ja loetakse väärtused muutujasse
        self.frame_top, self.frame_bottom, self.frame_image = self.create_two_frames()  # muutujate järjekord on oluline kui tagastatakse mitu asja ↓ vt funkts.
        # siin kolm muutuja nime on muutunud, tagastamisel ei ole oluline milline on nimi. neied nimesid kasutatakse edaspidi

        # pilt mida hatakse näitam aknas
        self.image = ImageTk.PhotoImage(Image.open(self.model.image_files[len(self.model.image_files)-1]))  # nimekirjast viimane pilt mis võtab
                                                # see on list self.model.image_files[len(self.model.image_files)-1] ja võtab listi viimase elemendi
                                                # vt. model.image_files asub funkts. väljakutsumine
        self.label_image = None


        # Create all Buttons, Labels and Entry, teeb kolm meetodit, teeme meetodi kus tehakse kõik nupu ↓
        # töö põhimõte, all tehakse meetod, mis tagastav (väljastab) nupud, siin kutsutakse meetod välja ja loetakse väärtused muutujasse
        self.btn_new, self.btn_cancel, self.btn_send = self.create_all_buttons()
        self.lbl_error, self.lbl_time, self.lbl_result = self.create_all_labels()
        self.char_input = self.create_input_entry()  # send nupu kõrval olev teksti kast

        # enter klahviga saab send nuppu käivitada
        # self.bind('<Return>', lambda event: self.controller.click_btn_send())  # event võib olla suvaline nimi, send() sulud peavad olema
        # '<Return>' on klahvi nimi, mis määrab millinse klahviga klaviatuurilt saab nuppu vajutada
        # probleem, et klahvi vajutus mõjub kogu aknale, vaja teha kontroll, kas mäng käib, siis võiks töötada


    def main(self):
        self.mainloop()  # GUI lõpulause mis hoiab akent ees


    @staticmethod
    def center(win):  # muutumatu funkts
        """
        https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def create_two_frames(self):
        frame_top = Frame(self, bg='#0096FF', height=50)  # blue
        frame_bottom = Frame(self, bg='#EBEB00')  # yellow

        frame_top.pack(fill=BOTH)  # asetab ekraanile
        frame_bottom.pack(expand=True, fill=BOTH)  # asetab ekraanile

        # poomise pilt
        frame_img = Frame(frame_top, bg='white', width=130, height=130)  # pannakse ülemisele paneelile - frame top
        frame_img.grid(row=0, column=3, rowspan=4, padx=5, pady=5)  # ühes reas kolmaselement, rowspan mergeb neli rida

        return frame_top, frame_bottom, frame_img  # tagastab kaks väärtust, kinnipüüdmisel vaja ka kaks muutujat, kolmas tuli juurde

    def create_all_buttons(self):  # osad nupud vaja ka tagastada, üks nupp on paigal ja rohkem ei puutu
        # New Game nupp
        btn_new = Button(self.frame_top, text='New Game', font=self.default_style, command=self.controller.click_btn_new)  # frame top on muutuja ülevalt
        Button(self.frame_top, text='Leaderboard', font=self.default_style,
               command=self.controller.click_btn_leaderboard).grid(row=0, column=1, padx=5, pady=2,  # grid teeb paigutuse
                                                                                 sticky=EW)  # see nupp ei muutu staatuselt (ei muutu halliks) saab
                                                                                            # alati klikkida selle pärast ei ole muutujas
        btn_cancel = Button(self.frame_top, text='Cancel', font=self.default_style, state='disabled',
                            command=self.controller.click_btn_cancel)  # mängu alguses ei saa klikkida state disabled
                                                # command= KKKKKÜÜÜÜSIMUUSSSS command= käivitab funkts, kui nupule vajutada
                                                # kui command= on puudu siis nupp ei tee midagi
                                                # kui tahad funkt midagi kaasa anda siis vaja lamdat kasutada
        btn_send = Button(self.frame_top, text='Send', font=self.default_style, state='disabled',
                          command=self.controller.click_btn_send)  # mängu alguses ei saa klikkida state disabled
                                            # font= stiilid on defineeritud konstruktoris
        # Button(self.frame_top, text='End', font=self.default_style,
                            #command=self.controller.click_btn_end).grid(row=0, column=3, padx=5, pady=2,
                                                                                 #sticky=EW) # Lõpetab mängu
        # Nuppude paigutus ekraanile
        btn_new.grid(row=0, column=0, padx=5, pady=2, sticky=EW)  # kõik nupud mis on framel paigutatakse gridiga
        btn_cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)  # kõik nupud mis on framel paigutatakse gridiga
        btn_send.grid(row=1, column=2, padx=5, pady=2, sticky=EW)  # kõik nupud mis on framel paigutatakse gridiga
        # nupud vaja ka tagastada
        return btn_new, btn_cancel, btn_send

        # teeb teksti väljad
    def create_all_labels(self):
        Label(self.frame_top, text='Input character', font=self.default_style_bold).grid(row=1, column=0, padx=5, pady=2)# luukase, pannakse paika, tagastamist vaja ei ole > ei muutu
        lbl_error = Label(self.frame_top, text='Wrong 0 letters(s)', anchor='w', font=self.default_style_bold)  # näitab millised valed tähed on sisestatud
        lbl_time = Label(self.frame_top, text='0:00:00', font=self.default_style)  # jookseb aeg
        lbl_result = Label(self.frame_bottom, text='Let\'s play'.upper(), font=self.big_font_style)  # näitab tulemust

        # on eraldi read kuna tahame muuta, paigutamine ekraanile ei saa kirjutada
        lbl_error.grid(row=2, column=0, columnspan=3, sticky=EW, padx=5, pady=2)  # pannakse üle kolme veeru merge
        lbl_time.grid(row=3, column=0, columnspan=3, sticky=EW, padx=5, pady=2)
        lbl_result.pack(padx=5, pady=2)  # on pack kuna läheb alumisele paneelile ja midagi gridi vaja ei ole kun teisi elemente ei ole

        #Pildi label
        self.label_image = Label(self.frame_image, image=self.image)
        self.label_image.pack()  # paneb ekraanile

        return lbl_error, lbl_time, lbl_result  # tagastab kolm muutujat

    def create_input_entry(self):
        char_input = Entry(self.frame_top, textvariable=self.userinput, justify='center', font=self.default_style) # on vaja mujal siis läheb muutujasse,
                                                            # textvariable=self.userinput muutuja konst
        char_input['state'] = 'disabled'
        char_input.grid(row=1, column=1, padx=5, pady=2)

        return char_input

    def change_image(self, image_id):  # vaja teada mitmendat pilti on vaja
        self.image = ImageTk.PhotoImage(Image.open(self.model.image_files[image_id]))  # mitmes pilt listist võtta
        # vt funkt create_all_labels rida 107 seal luuakse label_image
        self.label_image.configure(image=self.image)  # seadistab pildi aga ei näita
        self.label_image.image = self.image  # muudab pildi ekraanil näitab pilti

    # loome hüpikakna mille peale tabelit luuakse
    def create_popup_window(self):
        top = Toplevel(self)
        top.geometry('500x180')
        top.resizable(False, False)
        top.grab_set()  # alumist akent ei saa näppida kuni pealmine on kinni pandud
        top.focus()

        frame = Frame(top)
        frame.pack(expand=True, fill=BOTH)
        self.center(top)  # ekraani keskel üleval aknas
        # tegime akna , akna peale pannakse frame ja frame tagastatakse
        return frame

    def generate_leaderboard(self, frame, data):
        # tabeli vaade
        my_table = ttk.Treeview(frame)  # from tkinter import ttk

        # vertikaalne kerimis riba
        vsb = ttk.Scrollbar(frame, orient='vertical', command=my_table.yview)
        vsb.pack(side='right', fill='y')
        my_table.configure(yscrollcommand=vsb.set)

        # columns id
        my_table['columns'] = ('date_time', 'name', 'word', 'misses', 'game_time')

        # veergude omadused
        my_table.column('#0', width=0, stretch=NO)  # esimene veerg on peidetud veerg
        my_table.column('date_time', anchor=CENTER, width=90)
        my_table.column('name', anchor=CENTER, width=90)
        my_table.column('word', anchor=CENTER, width=90)
        my_table.column('misses', anchor=CENTER, width=90)
        my_table.column('game_time', anchor=CENTER, width=90)

        # tabeli päised
        my_table.heading('#0', text='', anchor=CENTER)
        my_table.heading('date_time', text='Date', anchor=CENTER)
        my_table.heading('name', text='Player', anchor=CENTER)
        my_table.heading('word', text='Word', anchor=CENTER)
        my_table.heading('misses', text='Wrong letters', anchor=CENTER)
        my_table.heading('game_time', text='Time', anchor=CENTER)

        # lisa andmed tabelisse
        x = 0
        for p in data:
            dt = datetime.strptime(p.date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %T')  # kuupäev luda ja vormistada teistpidi
            # info lisada tabelisse
            my_table.insert(parent='', index='end', iid=str(x), text='', values=(dt, p.name, p.word, p.misses,
                                                                                 str(timedelta(seconds=p.time))))  # index end lisab tabeli lõppu
            x += 1

        # kogu tabel on vaja frame peale panna
        my_table.pack(expand=True, fill=BOTH)