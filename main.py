import random
import time
import nltk
from nltk.corpus import words
from tkinter import *


# Download dictionary (only once)
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


class TypingSpeedApp:

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.current_index = -1
        self.canvas_text = None
        self.typed_text = ""
        self.phrase_list = []
        self.clicked = False
        self.word_list = words.words()
        self.filtered_word_list = [word for word in self.word_list if len(word) <= 6 and len(word) > 1]
        self.phrase_generator()
        self.start_time = None
        self.time_capacity = 30
        self.user_words = []


        user_entry.bind('<Key>', self.start_count)

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
            root.after(1000, self.countdown, timer - 1)
        else:
            time_var.set("Time's up!")
            user_entry.delete(0, 'end')
            user_entry.config(state="disabled")
            self.update_metrics()

    def update_metrics(self):
        for word in self.user_words:
            self.typed_text += str(word)
        elapsed_time = time.time() - self.start_time
        char_count = len(self.typed_text)
        cpm = (char_count / elapsed_time) * 60
        cpm_var.set(f"{cpm:.2f}")
        wpm = ((char_count / 5) / elapsed_time) * 60
        wpm_var.set(f"{wpm:.2f}")

        print(self.start_time)
        print(time.time())
        print(f"Ex: {elapsed_time}")
        print(self.phrase_list)
        print(self.user_words)

    def phrase_generator(self):
        self.phrase = ""
        for _ in range(10):
            random_word = random.choice(self.filtered_word_list)
            self.phrase += str(random_word).lower() + " "
            self.phrase_list.append(str(random_word).lower())
        # Display the generated phrase
        canvas_text = self.canvas.create_text(500, 225, text=self.phrase, font=('Helvetica', 20), tag="canvas_txt")
        return canvas_text

    def add_user_word(self, event):
        self.current_index += 1

        print(self.current_index)
        if user_entry.get().strip() != "":
            word = user_entry.get().strip()
            self.user_words.append(word)
            if word in self.phrase_list[self.current_index]:
                self.canvas.config(bg="lightgreen")
            else:
                self.canvas.config(bg='lightcoral')
            user_entry.delete(0, 'end')

            if self.current_index == 9:
                self.current_index = -1
                canvas.delete("canvas_txt")
                self.canvas.config(bg='lightblue')
                self.phrase_list.clear()
                self.user_words.clear()
                self.phrase_generator()

    def show_last_word(self, event):
        if user_entry.get() == " ":
            self.current_index -= 1
            text = self.user_words[-1]
            user_entry.insert(0, text)
            self.user_words.pop()
            print(text)


if __name__ == "__main__":
    app = TypingSpeedApp(root, canvas)
    root.mainloop()


# TODO 3: Underline current word to write inside Entry
# TODO 4: Add restart button to program
# TODO 5: Better phrase generate (easier to write) - another dictionary?
# TODO 6: Adjustment the program design
# TODO 7: If I type only one letter (like "e") there is possibility to achieve green background - bug!
# TODO 8: After 3 words there should be updating WPM and CMP
