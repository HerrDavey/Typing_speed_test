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

user_entry = Entry(frame, width=40, font='Helvetica 25 bold', justify='center')
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

    def __init__(self, root):
        self.root = root
        self.typed_text = ""
        self.clicked = False

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


if __name__ == "__main__":
    app = Typing_Speed_App(root)
    root.mainloop()

#def delete_entry(event):
# user_entry.delete(0, "end")
#
# # Dictionary settings
# word_list = words.words()
# filtered_word_list = [word for word in word_list if len(word) <= 6 and len(word) > 1]
#
# # Random Phrase generator
# phrase = ""
# for _ in range(10):
#     random_word = random.choice(filtered_word_list)
#     phrase += str(random_word).lower() + " "
# phrase_list = phrase.strip().split()
#
# # Create individual words on canvas
# word_ids = []
# x, y = 65, 80
# for word in phrase_list:
#     word_id = canvas.create_text(x, y, text=word, font=('Helvetica 25 bold'), anchor="nw", fill="black")
#     word_ids.append(word_id)
#     x += canvas.bbox(word_id)[2] - canvas.bbox(word_id)[0] + 10  # Move x by the width of the word + a space
#     if x > 850:  # Move to next line
#         x = 65
#         y += 40
#
#
# def process(event=None):
#     content = user_entry.get().strip().split()
#     for idx, word in enumerate(content):
#         if idx < len(phrase_list):
#             if word == phrase_list[idx]:
#                 canvas.itemconfig(word_ids[idx], fill="green")
#             else:
#                 canvas.itemconfig(word_ids[idx], fill="red")
#
#     for idx in range(len(content), len(phrase_list)):
#         canvas.itemconfig(word_ids[idx], fill="black")
#
#

#
#
# user_entry.bind('<space>', process)
