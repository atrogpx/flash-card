from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
index = None
to_learn = {}
current_card = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card.itemconfig(card_images, image=card_front)
    card.itemconfig(language, text="French", fill="black")
    card.itemconfig(word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card.itemconfig(card_images, image=card_back)
    card.itemconfig(language, text="English", fill="white")
    card.itemconfig(word, text=current_card["English"], fill="white")


def update_words():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')

card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_images = card.create_image(400, 263, image=card_front)
language = card.create_text(400, 150, font=("Ariel", 25, "italic"))
word = card.create_text(400, 263, font=("Ariel", 34, "bold"))
card.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=update_words)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
