from datetime import datetime


class GameTime:

    def __init__(self, label_time):
        self.label_time = label_time
        self.counter = 0  # loeb kulunud aega
        self.running = False

    def update(self):  # iga sekundi tagant numbri väärtus kasvab
        if self.running:
            if self.counter == 0:
                display = '0:00:00'
            else:
                tt = datetime.utcfromtimestamp(self.counter)
                string = tt.strftime('%T')  # %T kogu kuupäev %H:%M:%S
                display = string

            self.label_time['text'] = display  # labeli
            self.label_time.after(1000, self.update)  # kutsub välja 1 sek tagant seda sama funktsooni update
            self.counter += 1  # see vormistatakse ajaks ja vormindatakse

    def start(self):  # aja lugemise käivitamine
        self.running = True
        self.update()  # kutsub meetodi

    def stop(self):  # peatab aja lugemise
        self.running = False  # siis update enam ei kävitu

    def reset(self):  # aja lugemise reset
        self.counter = 0
        self.label_time['text'] = '0:00:00'