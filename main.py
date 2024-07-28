import random
import time
import tkinter.messagebox

import nltk
import json
from nltk.corpus import words
from nltk.data import find
from tkinter import *


# Download dictionary (only once)
def download_dictionary():
    try:
        find('corpora/words.zip')
    except LookupError:
        tkinter.messagebox.showinfo("Downloading...", 'Downloading dictionary please wait')
        nltk.download('words')
        tkinter.messagebox.showinfo("Download successful", "Download successful")


# Window Settings
root = Tk()
root.geometry("1080x700")
root.maxsize(1080, 700)
root.title("Writing Speed Test App")
root.config(bg='#143F6B')
root.resizable(False, False)

# Elements in window
frame = Frame(root, height=200, width=1000, bg="#F55353")
frame.place(anchor="s", relx=.5, rely=.97)

canvas = Canvas(root, height=450, width=1000, bg="#FEB139", highlightthickness=0)
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

text_widget = Text(canvas, font='Helvetica 20 bold', bg='#FEB139', wrap='word', height=5, width=50,
                   highlightthickness=0, borderwidth=0)
text_widget.place(anchor="center", relx=.51, rely=.6)
text_widget.config(state=DISABLED)

restart_btn = Button(frame, text="Try again", highlightthickness=0, bd=2, bg="#000000", font='Helvetica 13 bold',
                     fg="#EEEEEE")
restart_btn.place(anchor="s", rely=.6, relx=.93)


class TypingSpeedApp:

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.current_index = -1
        self.highlight_index = 0
        self.canvas_text = None
        self.typed_text = ""
        self.phrase_list = []
        self.phrase_list_history = []
        self.clicked = False
        self.word_list = words.words()
        self.filtered_word_list = [word for word in self.word_list if 6 >= len(word) > 1][-666:]
        self.phrase_generator()
        self.start_time = None
        self.time_capacity = 60
        self.user_words = []
        self.user_words_history = []
        self.timer_id = None

        user_entry.bind('<Key>', self.start_count)
        restart_btn.config(command=self.restart)

    def start_count(self, event):
        if not self.clicked:
            self.clicked = True
            self.start_time = time.time()
            self.countdown(int(self.time_capacity - 1))
            user_entry.unbind('<Key>')

    def countdown(self, timer):
        if timer >= 0:
            mins, secs = divmod(timer, 60)
            formatted_time = '{:02d}:{:02d}'.format(mins, secs)
            time_var.set(formatted_time)

            user_entry.bind("<space>", self.add_user_word)
            user_entry.bind("<BackSpace>", self.show_last_word)
            self.timer_id = root.after(1000, self.countdown, timer - 1)
        else:
            time_var.set("Time's up!")
            user_entry.delete(0, 'end')
            user_entry.config(state="disabled")
            self.update_metrics()
            self.scoreboard_save()

    def update_metrics(self):
        elapsed_time = time.time() - self.start_time
        raw_cpm = (len(self.typed_text) / elapsed_time) * 60
        corrected_text = ' '.join(
            [word for word, correct in zip(self.user_words_history, self.phrase_list_history) if word == correct])
        corrected_cpm = (len(corrected_text) / elapsed_time) * 60
        wpm = corrected_cpm / 5

        cpm_var.set(f"{raw_cpm:.2f}")
        wpm_var.set(f"{wpm:.2f}")

    def phrase_generator(self):
        self.phrase = ""
        for _ in range(10):
            random_word = random.choice(self.filtered_word_list)
            self.phrase += str(random_word).lower() + " "
            self.phrase_list.append(str(random_word).lower())
            self.phrase_list_history.append(str(random_word).lower())
        self.display_phrase()
        self.highlight_next_word()

    def display_phrase(self):
        text_widget.config(state=NORMAL)
        text_widget.delete("1.0", END)
        text_widget.insert(END, self.phrase)
        text_widget.config(state=DISABLED)

    def add_user_word(self, event):
        typed_word = user_entry.get().strip()
        if typed_word:
            self.current_index += 1
            self.user_words.append(typed_word)
            self.user_words_history.append(typed_word)
            self.typed_text += typed_word + " "
            if typed_word == self.phrase_list[self.current_index]:
                self.canvas.config(bg="lightgreen")
                text_widget.config(bg='lightgreen')
            else:
                self.canvas.config(bg='lightcoral')
                text_widget.config(bg='lightcoral')
            user_entry.delete(0, 'end')

            if self.current_index == 9:
                self.current_index = -1
                self.highlight_index = 0
                canvas.delete("canvas_txt")
                self.canvas.config(bg='#FEB139')
                text_widget.config(bg='#FEB139')
                self.phrase_list.clear()
                self.user_words.clear()
                self.phrase_generator()
            else:
                self.highlight_next_word()

            if len(self.user_words) > 2:
                self.update_metrics()
        else:
            user_entry.delete(0, 'end')

    def show_last_word(self, event):
        if user_entry.get() == " ":
            self.current_index -= 1
            self.highlight_index -= 1
            self.highlight_previous_word()
            text = self.user_words[-1]
            user_entry.insert(0, text)
            self.user_words.pop()
            self.user_words_history.pop()
            self.highlight_next_word()

    def highlight_next_word(self):
        text_widget.tag_remove("highlight", "1.0", "end")

        words = self.phrase.strip().split()
        start_idx = sum(len(words[i]) + 1 for i in range(self.highlight_index))
        end_idx = start_idx + len(words[self.highlight_index])

        text_widget.config(state=NORMAL)
        text_widget.tag_add("highlight", f"1.{start_idx}", f"1.{end_idx}")
        text_widget.tag_config("highlight", background='#F6F54D')
        text_widget.config(state=DISABLED)
        self.highlight_index += 1

    def highlight_previous_word(self):
        self.highlight_index -= 1
        text_widget.tag_remove("highlight", "1.0", "end")
        words = self.phrase.strip().split()
        start_idx = sum(len(words[i]) + 1 for i in range(self.highlight_index))
        end_idx = start_idx + len(words[self.highlight_index])
        text_widget.config(state=NORMAL)
        text_widget.tag_add("highlight", f"1.{start_idx}", f"1.{end_idx}")
        text_widget.tag_config("highlight", background="yellow")
        text_widget.config(state=DISABLED)

    def restart(self):
        if self.timer_id:
            root.after_cancel(self.timer_id)
        self.clicked = False
        self.current_index = -1
        self.highlight_index = 0
        self.canvas_text = None
        self.typed_text = ""
        self.phrase_list.clear()
        self.phrase_list_history.clear()
        self.user_words.clear()
        self.user_words_history.clear()
        user_entry.config(state=NORMAL)
        user_entry.delete(0, 'end')
        time_var.set("1:00")
        cpm_var.set("?")
        wpm_var.set("?")
        self.phrase_generator()
        user_entry.bind('<Key>', self.start_count)
        self.canvas.config(bg='#FEB139')
        text_widget.config(bg='#FEB139')

    def scoreboard_save(self):
        new_score_cpm = float(cpm_var.get())
        new_score_wpm = float(wpm_var.get())

        try:
            with open('scoreboard.json', 'r+') as file:
                last_score = json.load(file)
                last_wpm = float(last_score["WPM"])
                last_cpm = float(last_score["CPM"])

                if new_score_cpm > last_cpm:
                    last_score["CPM"] = new_score_cpm

                if new_score_wpm > last_wpm:
                    last_score["WPM"] = new_score_wpm

                if new_score_cpm > last_cpm or new_score_wpm > last_wpm:
                    file.seek(0)
                    file.truncate(0)
                    json.dump(last_score, file)

                text_widget.config(state=NORMAL)
                text_widget.delete("1.0", END)
                text_widget.place(anchor="center", relx=.65, rely=.58)
                text_widget.insert(END, f"Time's up! Your best score was: "
                                        f"\n\nWPM: {last_wpm}  \n\nCPM: {last_cpm}")
                text_widget.config(state=DISABLED)

        except FileNotFoundError:
            with open('scoreboard.json', 'a') as file:
                max_value_cpm = cpm_var.get()
                max_value_wpm = wpm_var.get()
                score = {
                    "WPM": float(max_value_wpm),
                    "CPM": float(max_value_cpm)
                }
                json.dump(score, file)


if __name__ == "__main__":
    download_dictionary()
    app = TypingSpeedApp(root, canvas)
    root.mainloop()
