import time

import nltk
import random
import textwrap
from nltk.corpus import words
from tkinter import *

# Download dictonary (only once)
# nltk.download('words')

# Window Settings
root = Tk()
root.geometry("1080x700")
root.maxsize(1080, 700)
root.title("Writing Speed Test App")
root.config(bg="white")

# Elements in window
canvas = Canvas(root, height=450, width=1000, bg="lightblue", highlightthickness=0)
frame = Frame(root, height=150, width=1000, bg="yellow")
canvas.place(anchor="n", relx=.5, rely=.02)
frame.place(anchor="s", relx=.5, rely=.9)
user_entry = Entry(frame, width=40, font=('Helvetica 25 bold'), justify='center')
user_entry.place(anchor='center', rely=.2, relx=.5)


# Dictionary settings
word_list = words.words()
filtered_word_list = [word for word in word_list if len(word) <= 6 and len(word) > 1]

# Random Phrase generator
phrase = ""
for _ in range(50):
    random_word = random.choice(filtered_word_list)
    phrase += str(random_word).lower() + " "
phrase = textwrap.fill(phrase, width=50)
canvas.create_text(500, 200, text=phrase, font=('Helvetica 25 bold'), anchor="center")

def process(event=None):
    content = user_entry.get()
    if content == phrase.split(" ")[0]:
        print("O MAJJJ GAAD")

user_entry.bind('<space>', process)




# # Variables to track user input
# input_text = ""
# current_index = 0
# def on_key_press(event):
#     global input_text, current_index
#
#     if current_index < len(phrase) and event.char == phrase[current_index]:
#         current_index += 1
#         root.config(bg="green")
#     else:
#         root.config(bg="red")
#
#     input_text += event.char
#
#     # Reset background color after a short delay
#     root.after(100, lambda: root.config(bg="white"))
#
#
# # Bind the key press event
# root.bind("<KeyPress>", on_key_press)
# canvas.focus_set()

# Start function
root.mainloop()
