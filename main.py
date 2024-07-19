import random
import time
import nltk
from nltk.corpus import words
from tkinter import *


# Download dictonary (only once)
def download_dictionary():
    nltk.download('words')


# Window Settings
root = Tk()
root.geometry("1080x700")
root.maxsize(1080, 700)
root.title("Writing Speed Test App")
root.config(bg="white")
root.resizable(False, False)

# Elements in window
frame = Frame(root, height=200, width=1000, bg="yellow")
frame.place(anchor="s", relx=.5, rely=.97)

canvas = Canvas(root, height=450, width=1000, bg="lightblue", highlightthickness=0)
canvas.place(anchor="n", relx=.5, rely=.02)

user_entry = Entry(frame, width=40, font='Helvetica 25', justify='center')
user_entry.place(anchor='center', rely=.2, relx=.5)

time_var = StringVar()
time_var.set("1:00")
time_label = Label(frame, width=12, textvariable=time_var, font='Helvetica 12 bold', bg="white", highlightthickness=2)
time_label.place(anchor="s", rely=.6, relx=.22)

cpm_var = StringVar()
cpm_var.set("?")
cpm_label = Label(frame, width=12, textvariable=cpm_var, font='Helvetica 12 bold', bg="white", highlightthickness=2)
cpm_label.place(anchor="s", rely=.6, relx=.5)

wpm_var = StringVar()
wpm_var.set("?")
wpm_label = Label(frame, width=12, textvariable=wpm_var, font='Helvetica 12 bold', bg="white", highlightthickness=2)
wpm_label.place(anchor="s", rely=.6, relx=.77)

label_time = Label(frame, font='Helvetica 10 bold', bg="lightblue", text="Timer")
label_time.place(anchor="s", rely=.75, relx=.22)

label_cpm = Label(frame, font='Helvetica 10 bold', bg="lightblue", text="CPM")
label_cpm.place(anchor="s", rely=.75, relx=.5)

label_wpm = Label(frame, font='Helvetica 10 bold', bg="lightblue", text="WPM")
label_wpm.place(anchor="s", rely=.75, relx=.77)


class Typing_Speed_App:

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.typed_text = ""
        self.clicked = False
        self.word_list = words.words()
        self.filtered_word_list = [word for word in self.word_list if len(word) <= 6 and len(word) > 1]
        self.phrase_generator()


        user_entry.bind('<Key>', self.start_count)

    def start_count(self, event):
        if not self.clicked:
            self.clicked = True
            self.countdown(int(10))
            event.widget.unbind('<Key>')

    def countdown(self, timer):
        if timer >= 0:
            mins, secs = divmod(timer, 60)
            formatted_time = '{:02d}:{:02d}'.format(mins, secs)
            time_var.set(formatted_time)
            root.after(1000, self.countdown, timer - 1)
        else:
            time_var.set("Time's up!")
            user_entry.config(state="disabled")
            self.update_metrics()

    def update_metrics(self):
        self.typed_text = str(user_entry.get())
        elapsed_time = 10
        char_count = len(self.typed_text)
        cpm = char_count / elapsed_time
        cpm_var.set(f"{cpm:.2f}")
        wpm = (char_count / 5) / elapsed_time
        wpm_var.set(f"{wpm:.2f}")

    def phrase_generator(self):
        self.phrase = ""
        for _ in range(10):
            random_word = random.choice(self.filtered_word_list)
            self.phrase += str(random_word).lower() + " "
        self.phrase_list = self.phrase.strip().split()

        # Display the generated phrase
        self.canvas.create_text(500, 225, text=self.phrase, font=('Helvetica', 20))
        print(self.phrase_list)

if __name__ == "__main__":
    app = Typing_Speed_App(root, canvas)
    root.mainloop()


