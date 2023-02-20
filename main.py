import random
from tkinter import *
from tkinter.ttk import Combobox

import pandas

window = Tk()
window.title("Flash card")

window.config(padx=20, pady=20)
window.config(bg="#B1DDC6")
from_language = Combobox(window, width=60, values=["Arabic", "French"])
from_language.grid(row=0,column=1, columnspan=2, sticky="")






flash_card = Canvas(width=800, height=526)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card = flash_card.create_image(400, 263, image=card_front)
current_title = flash_card.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
current_word = flash_card.create_text(400, 263, text="Word", font=("Arial", 75, "bold"))
flash_card.grid(row=2, column=1, columnspan=2)
flash_card.config(bg="#B1DDC6", highlightthickness=0)
flash_card.config()

from_label = Label(text="Choose the language:", font=("Arial", 12))
from_label.config(bg="#B1DDC6", padx=25)
from_label.grid(row=0, column=0, sticky="N")

right_button_img = PhotoImage(file='right.png')
wrong_button_img = PhotoImage(file='wrong.png')
flip_button_img = PhotoImage(file='flip.png')
flip_resize = flip_button_img.subsample(5, 5)
got_it = PhotoImage(file='got_it.png')
got_it_resized = got_it.subsample(7, 7)
not_it = PhotoImage(file='not_it.png')
not_it_resized = not_it.subsample(6, 6)

not_it_list_un_formatted = []
not_it_list = []
got_it_list = []
shown_words = []

def get_data():
    value = from_language.get()
    if value == "Arabic":
        file = "book8_copy.csv"
        flashcard_run(file, "Arabic", "English")
    elif value == "French":
        file = "french_words.csv"
        flashcard_run(file, "French", "English")


start_button = Button(text="Start", command=get_data)
start_button.grid(row=0, column=3, padx=60, sticky="N")
def flashcard_run(file, lan_a_title, lan_b_title):
    data = pandas.read_csv(file)
    words_dict = data.to_dict(orient="records")
    lan_a_title = lan_a_title
    lan_b_title = lan_b_title


    def pick_word():
        word = random.choice(words_dict)
        if word in shown_words:
            word = random.choice(words_dict)
        flash_card.itemconfig(card, image=card_front)
        flash_card.itemconfig(current_word, fill="black", font=("Arial", 75, "bold"))
        flash_card.itemconfig(current_word, text=(word['lan_a']))
        flash_card.itemconfig(current_title, text=lan_a_title)
        shown_words.append(word)


    def wrong_button_f():
        word_on = flash_card.itemcget(current_word, 'text')
        for i in range(len(words_dict)):
            if words_dict[i]["lan_a"] == word_on:
                not_it_list.append(words_dict[i])
                flash_card.itemconfig(current_word, fill="#EB455F", font=("Arial", 75, "bold"))


    def got_it_button_f():
        for word in (shown_words):
            if word not in (not_it_list) and word not in (got_it_list):
                got_it_list.append(word)
        list_output(got_it_list)


    def list_output(list):
        global pop
        pop = Toplevel(window)
        row_height = 50
        pop.geometry(f"700x{len(list) * row_height}")
        row = 0
        for item in list:
            output = (f"{(item['lan_a'])} : {(item['lan_b'])}")
            pop_label = Label(pop, text=str(output), font=("Arial", 22, "normal"), wraplength=700)
            pop_label.grid(row=row, column=0, sticky='w')
            row += 1


    def flip_card():
        word_on = flash_card.itemcget(current_word, 'text')

        for i in range(len(words_dict)):

            if words_dict[i]["lan_a"] == word_on:
                flash_card.itemconfig(card, image=card_back)
                flash_card.itemconfig(current_title, text=lan_b_title, font=("Arial", 32, "italic"))
                flash_card.itemconfig(current_word, text=words_dict[i]["lan_b"])
                flash_card.itemconfig(current_word, font=("Arial", 32, "bold"))
            elif words_dict[i]["lan_b"] == word_on:
                flash_card.itemconfig(card, image=card_front)
                flash_card.itemconfig(current_title, text=lan_a_title, font=("Arial", 32, "italic"))
                flash_card.itemconfig(current_word, text=words_dict[i]["lan_a"])
                flash_card.itemconfig(current_word, font=("Arial", 75, "bold"))


    not_it_wrong = Button(text="Not it", image=not_it_resized, highlightthickness=0,
                          command=lambda: list_output(not_it_list))
    not_it_wrong.grid(row=2, column=0, )

    got_it_right = Button(text="Got it", image=got_it_resized, highlightthickness=0,
                          command=got_it_button_f)
    got_it_right.grid(row=2, column=3, )

    wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=wrong_button_f)
    wrong_button.grid(row=3, column=0)
    flip_button = Button(image=flip_resize, highlightthickness=0, command=flip_card)
    flip_button.grid(row=3, column=1, columnspan=2)
    correct_button = Button(image=right_button_img, highlightthickness=0, command=pick_word)
    correct_button.grid(row=3, column=3)











window.mainloop()
