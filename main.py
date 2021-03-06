import string
import random
import threading
import time

from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
from english_words import english_words_lower_alpha_set

root = Tk()
root.title("SpeedTyper")
root.configure(bg="white")

root.state("zoomed")


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)



class SpeedTyper:

    def __init__(self, player="Player", rounds=10):
        self.player = player
        self.rounds = rounds
        self.alphabet = string.ascii_uppercase
        self.finished_rounds = 0
        self.mistakes = 0
        self.first_iter = True
        self.exit_event = threading.Event()
        self.level = StringVar()
        self.objective = random.randint(1, 50)
        self.congratulations_msg = ['Congrats!', "Rock'on!", "Nice!", "Easy ಠ_ಠ", "Magic?", "Glory!"]

        # Sound paths
        self.correct_sounds = [r'Sounds/Correct.mp3', r'Sounds/Correct1.mp3', r'Sounds/Correct2.mp3']
        self.music_status = True

        # Sound images
        sound_on_load = Image.open(r'Graphics/sound_on.png')
        self.sound_on = ImageTk.PhotoImage(sound_on_load.resize((100, 50), Image.ANTIALIAS))

        sound_off_load = Image.open(r'Graphics/sound_off.png')
        self.sound_off = ImageTk.PhotoImage(sound_off_load.resize((100, 50), Image.ANTIALIAS))

        sound_on_inversed_load = Image.open(r'Graphics/sound_on_inversed.png')
        self.sound_on_inversed = ImageTk.PhotoImage(sound_on_inversed_load.resize((100, 50), Image.ANTIALIAS))

        sound_off_inversed_load = Image.open(r'Graphics/sound_off_inversed.png')
        self.sound_off_inversed = ImageTk.PhotoImage(sound_off_inversed_load.resize((100, 50), Image.ANTIALIAS))

        # Words
        self.word_list = list(english_words_lower_alpha_set)

        self.letters_or_words = StringVar()

        #Settings menu initial status
        self.settings_status = False

    def check(self, *args):

        txt = self.input_box.get().upper()

        if txt == self.choice.upper():

            self.input_box.delete(0, "end")

            if self.letters_or_words.get() == 'letters':
                self.choice = random.choice(self.alphabet)
            else:
                self.choice = random.choice(self.word_list)

            self.letter["text"] = self.choice
            self.finished_rounds += 1
            if self.finished_rounds == self.objective:
                self.objectives_label['text'] = 'Objective: {obj} || Reached!'.format(obj=self.objective)
            self.victories["text"] = 'Points: {points}/{obj}'.format(points=self.finished_rounds, obj=self.objective)

            if self.music_status:
                correct = threading.Thread(target=self.correct_sound)
                correct.start()

        elif len(txt) < len(self.choice):
            pass

        else:
            print(txt)
            print(self.choice)
            self.mistakes += 1
            self.mistakes_label['text'] = 'Typos: {mistakes}'.format(mistakes=self.mistakes)
            self.input_box.delete(0, "end")

            if self.music_status:
                wrong = threading.Thread(target=self.mistake_sound)
                wrong.start()

    def mistake_sound(self):
        playsound('Sounds/Wrong.mp3')

    def correct_sound(self):
        playsound(random.choice(self.correct_sounds))

    def time_up_sound(self):
        playsound('Sounds/TimesUp.mp3')

    def switch_music(self):
        self.music_status = not self.music_status
        if self.music_status:
            self.music_display.configure(image=self.sound_on)
        else:
            self.music_display.configure(image=self.sound_off)

    def music_image_switch(self, e):
        if self.music_status:
            self.music_display.configure(image=self.sound_on_inversed)
        else:
            self.music_display.configure(image=self.sound_off_inversed)

    def music_image_switch_exit(self, e):
        if self.music_status:
            self.music_display.configure(image=self.sound_on)
        else:
            self.music_display.configure(image=self.sound_off)

    def main_GUI(self):



        #Right side Frame (All columns except 0)
        self.side_frame = Frame(root, bg='white')
        self.side_frame.grid(row=0, column=1)
        self.side_frame.bind('<Enter>', self.menu_leave)

        #First column frame
        self.column1_frame = Frame(root, bg='white')
        self.column1_frame.grid(row=0, column=0)


        # Logo
        logo_load = Image.open(r'Graphics/racecar.png')
        logo_img = ImageTk.PhotoImage(logo_load.resize((300, 200), Image.ANTIALIAS))

        logo = Button(self.column1_frame, image=logo_img, bd=0, highlightthickness=0)
        logo.image = logo_img


        logo.bind('<Enter>', lambda x: self.menu_enter())

        #Stat widets
        self.stats = Frame(self.column1_frame, bg='white', highlightbackground='cyan', highlightthickness=1)
        self.victories = Label(self.stats, text="Points: 0", fg="Cyan", bg="White", font=("Arial", 50), padx=15)
        self.mistakes_label = Label(self.stats, text='Typos: 0', bg='white', fg='cyan', font=("Arial", 50))
        self.objectives_label = Label(self.stats, text='Objective: X', bg='white', fg='gold', font=("Arial", 15),
                                      justify=LEFT, anchor='w')

        #Other widgets
        title = Label(self.side_frame, text="Speed Typer", bg="white", fg="cyan", font=("Bauhaus 93", 100))
        self.letter = Label(self.side_frame, text="", bg="white", fg="cyan", font=("Copperplate Gothic Bold", 50))
        self.input_box = Entry(self.side_frame, bg="white", fg="cyan", font=("Copperplate Gothic Bold", 50), justify=CENTER, width=10)
        self.input_box.bind('<KeyRelease>', self.check)
        self.new_game_button = Button(self.side_frame, fg='Cyan', bg='white', text='New Game!', font=("Bauhaus 93", 50), command=lambda: self.new_game())
        self.timer = Label(self.column1_frame, text=30, bg='white', fg='cyan', font=("Arial", 50))

        #Turn on and off music

        self.music_display = Button(self.side_frame, image=self.sound_on, fg='cyan', bg='white', command=self.switch_music,
                                    bd=0, highlightthickness=0)
        self.music_display.grid(row=1, column=3, padx=10, pady=10)
        self.music_display.bind('<Enter>', self.music_image_switch)
        self.music_display.bind('<Leave>', self.music_image_switch_exit)


        #Level selector
        self.levels = Frame(self.column1_frame, bg='white')

        self.beginner = Radiobutton(self.levels, text='Beginner', variable=self.level, value='beginner', bg='white', font=("Arial", 15), fg='cyan',
                                    command=lambda: self.set_objective())
        self.beginner.bind('<Enter>', lambda x: self.beginner.configure(fg='white', bg='cyan'))
        self.beginner.bind('<Leave>', lambda x: self.beginner.configure(fg='cyan', bg='white'))

        self.intermediate = Radiobutton(self.levels, text='Intermediate', variable=self.level, value='intermediate', bg='white', font=("Arial", 15), fg='cyan',
                                        command=lambda: self.set_objective())
        self.intermediate.bind('<Enter>', lambda x: self.intermediate.configure(fg='white', bg='cyan'))
        self.intermediate.bind('<Leave>', lambda x: self.intermediate.configure(fg='cyan', bg='white'))

        self.expert = Radiobutton(self.levels, text='Expert', variable=self.level, value='expert', bg='white', font=("Arial", 15), fg='cyan',
                                  command=lambda: self.set_objective())
        self.expert.bind('<Enter>', lambda x: self.expert.configure(fg='white', bg='cyan'))
        self.expert.bind('<Leave>', lambda x: self.expert.configure(fg='cyan', bg='white'))


        #placing widgets
        title.grid(row=0, column=2, padx=10, pady=10, columnspan=2)
        self.letter.grid(row=1, column=2)
        self.input_box.grid(row=2, column=2, padx=10, pady=10, ipady=45)
        self.timer.grid(row=1, column=1)
        self.new_game_button.grid(row=3, column=2, padx=10, pady=10)

        #Placing stats
        self.stats.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.victories.grid(row=0, column=0)
        self.objectives_label.grid(row=1, column=0, sticky=W, padx=15)
        self.mistakes_label.grid(row=2, column=0)

        #Placing levels
        self.levels.grid(row=1, column=0)

        self.beginner.grid(row=0, column=0)
        self.intermediate.grid(row=1, column=0)
        self.expert.grid(row=2, column=0)

        #self.bot.grid(row=3, column=0, padx=10, pady=10)
        logo.grid(row=0, column=0, columnspan=2)

        self.new_game_button.bind('<Enter>', lambda x: self.new_game_button.configure(fg='white', bg='cyan'))
        self.new_game_button.bind('<Leave>', lambda x: self.new_game_button.configure(fg='cyan', bg='white'))

        # Words or letters

        self.word_type = Frame(self.column1_frame, bg='white')
        self.words_box = Radiobutton(self.word_type, text='Words', bg='white', font=("Arial", 15), fg='cyan', variable=self.letters_or_words, value='words',
                                     command=self.new_game)
        self.letter_box = Radiobutton(self.word_type, text='Letters', bg='white', font=("Arial", 15), fg='cyan', variable=self.letters_or_words, value='letters',
                                      command=self.new_game)

        self.word_type.grid(row=3, column=0)
        self.words_box.grid(row=0, column=0)
        self.letter_box.grid(row=1, column=0)

        self.words_box.bind('<Enter>', lambda x: self.words_box.configure(bg='cyan', fg='white'))
        self.words_box.bind('<Leave>', lambda x: self.words_box.configure(bg='white', fg='cyan'))

        self.letter_box.bind('<Enter>', lambda x: self.letter_box.configure(bg='cyan', fg='white'))
        self.letter_box.bind('<Leave>', lambda x: self.letter_box.configure(bg='white', fg='cyan'))

        self.settings = Frame(self.column1_frame, bg='white')

        # Set custom time
        self.custom_time_title = Label(self.settings, text="Set a custom time: ", fg="cyan", bg='white',
                                       font=("Arial", 15))

        self.custom_time_entry = Entry(self.settings, bg='white', font=("Arial", 15), fg='cyan', validate='key')
        self.custom_time_entry.configure(validatecommand=(self.custom_time_entry.register(self.validate), '%P','%d'))

        self.set_custom_time = Button(self.settings, bg='white', text="Set new time", command=self.new_game, fg='cyan', font=("Arial", 15))
        self.set_custom_time.bind('<Enter>', lambda x: self.set_custom_time.configure(bg='cyan', fg='white'))
        self.set_custom_time.bind('<Leave>', lambda x: self.set_custom_time.configure(bg='white', fg='cyan'))

    def validate(self, inStr,acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit() or len(self.custom_time_entry.get()) > 5:
                return False
        return True

    def bot_opponent(self):
        if self.level.get() == 'beginner':
            self.bot_point_ratio = random.randint(3, 15)
        elif self.level.get() == 'intermediate':
            self.bot_point_ratio = random.randint(15, 35)
        elif self.level.get() == 'expert':
            self.bot_point_ratio = random.randint(35, 60)


    def set_objective(self):

        #Function gets called when radiobutton level is updated

        #Reset scored points and typos
        self.finished_rounds = 0
        self.mistakes = 0

        #Set new objective
        if self.level.get() == 'beginner':
            self.objective = random.randint(3, 15)

        elif self.level.get() == 'intermediate':
            self.objective = random.randint(15, 35)

        elif self.level.get() == 'expert':
            self.objective = random.randint(35, 60)
        else:
            self.objective = random.randint(5, 50)

        self.objectives_label['text'] = 'Objective: {obj}'.format(obj=self.objective)
        self.victories['text'] = 'Points: {points}/{obj}'.format(points=self.finished_rounds, obj=self.objective)
        self.mistakes_label['text'] = 'Typos: {typos}'.format(typos=self.mistakes)

    def new_game(self):
        self.input_box.delete(0, END)
        if not self.first_iter:
            self.exit_event.set()
            time.sleep(1)
            self.exit_event.clear()

        count = threading.Thread(target=lambda: self.countdown())
        count.start()
        if self.first_iter:
            self.first_iter = False

    def new_game_setup(self):
        # Reebind input keys
        self.input_box.bind('<KeyRelease>', self.check)

        # Reenable entry
        self.input_box.configure(state='normal')

        print("New game words: " + str(self.letters_or_words.get()))
        # First letter/word
        if self.letters_or_words.get() == 'letters':
            self.choice = random.choice(self.alphabet)
        else:
            self.choice = random.choice(self.word_list)

        self.letter["text"] = self.choice

        # Reset mistakes
        self.mistakes = 0
        self.mistakes_label['text'] = 'Typos: 0'

        # Set new objectif
        self.set_objective()

        # Reset victories
        self.finished_rounds = 0
        self.victories['text'] = "Points: 0/{obj}".format(obj=self.objective)
        self.input_box.focus()

        root.update()

    def countdown(self):

        if self.custom_time_entry.get() == '':
            allocated_time = 30
        else:
            allocated_time = int(self.custom_time_entry.get())

        self.input_box.configure(state='disabled')
        self.timer['text'] = allocated_time
        self.letter.configure(text=3, fg='gold')
        time.sleep(1)
        self.letter.configure(text=2)
        time.sleep(1)
        self.letter.configure(text=1)
        time.sleep(1)
        self.letter.configure(fg='cyan')

        #Start game
        self.new_game_setup()

        for i in reversed(range(allocated_time)):
            self.timer['text'] = i
            time.sleep(1)
            if self.exit_event.is_set():
                print("stopped")
                break

        if not self.exit_event.is_set():
            self.input_box.delete(0,  'end')
            self.input_box['state'] = 'disabled'
            self.input_box.unbind('<KeyRelease>')

            if self.finished_rounds >= self.objective:
                self.letter.configure(text=random.choice(self.congratulations_msg), fg='gold')
            if self.music_status:
                done_sound = threading.Thread(target=self.time_up_sound)
                done_sound.start()

    def menu_enter(self):
        if not self.settings_status:
            # remove from grid all widgets from column 0 and 1
            self.stats.grid_remove()
            self.levels.grid_remove()
            self.word_type.grid_remove()
            self.timer.grid_remove()

            self.column1_frame.configure(highlightbackground="cyan", highlightcolor="cyan", highlightthickness=10)
            #Add settings widgets
            self.settings.grid(row=1, column=0)
            self.custom_time_title.grid(row=0, column=0, padx=15, pady=15)
            self.custom_time_entry.grid(row=1, column=0, padx=15, pady=15, ipady=15)
            self.set_custom_time.grid(row=2, column=0, padx=15, pady=15)

            # Set settings status to open
            self.settings_status = True


    def menu_leave(self, _):
        if self.settings_status:
            #Remove widgets from menu
            self.settings.grid_forget()
            self.set_custom_time.grid_forget()
            self.custom_time_title.grid_forget()
            self.custom_time_entry.grid_forget()

            self.column1_frame.configure(highlightthickness=0)

            #Regrid the widgets removed in self.menu_enter()
            self.stats.grid(row=2, column=0)
            self.levels.grid(row=1, column=0)
            self.word_type.grid(row=3, column=0)
            self.timer.grid(row=1, column=1)

            # Set menu close
            self.settings_status = False



def main():
    game = SpeedTyper()
    game.main_GUI()
    game.new_game()



if __name__ == "__main__":
    main_process = Thread(target=lambda: main())
    main_process.start()

    mainloop()

