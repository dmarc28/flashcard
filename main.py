import random
from tkinter import *
from tkinter.ttk import Combobox
import textwrap

import pandas

window = Tk()
window.title("Flash card")

window.config(padx=20, pady=20)
window.config(bg="white")

from_label = Label(text="Choose the language:", font=("Arial", 12))
from_label.config(bg="white", padx=25, pady=25)
from_label.grid(row=0, column=0, sticky="N")

from_language = Combobox(window, values=["Arabic", "French"])
from_language.grid(row=0, column=1, columnspan=1, sticky="")

flash_card = Canvas(width=600, height=400, bg="white")

card_front = PhotoImage(file="icons/card_front.png")

card_back = PhotoImage(file="icons/card_back.png")

card = flash_card.create_image(300, 200, image=card_front)
current_title = flash_card.create_text(300, 60, text="Title", font=("Arial", 40, "italic"))
current_word = flash_card.create_text(300, 200, text="Word", font=("Arial", 75, "bold"))
flash_card.grid(row=3, column=0, columnspan=2)
flash_card.config(bg="white", highlightthickness=0)

right_button_img = PhotoImage(file='icons/next.png')
wrong_button_img = PhotoImage(file='icons/wrong.png')
wrong_button_img = wrong_button_img.subsample(2, 2)
flip_button_img = PhotoImage(file='icons/flip.png')
flip_resize = flip_button_img.subsample(2, 2)
got_it = PhotoImage(file='icons/Mastered_list.png')
got_it_resized = got_it.subsample(2, 2)
not_it = PhotoImage(file="icons/Review_list.png")
not_it_resized = not_it.subsample(2, 2)

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


start_icon = PhotoImage(file="icons/start.png")
start_button = Button(image=start_icon, command=get_data)
start_button.grid(row=1, column=0, columnspan=2, sticky="N")
start_button.config(pady=25)


def flashcard_run(file, lan_a_title, lan_b_title):
    data = pandas.read_csv(file)
    words_dict = data.to_dict(orient="records")
    lan_a_title = lan_a_title
    lan_b_title = lan_b_title
    first_word = words_dict[random.randint(0,15)]["lan_a"]
    print(first_word)
    flash_card.itemconfig(current_word, fill="black", font=("Arial", 75, "bold"))
    flash_card.itemconfig(current_word, text=first_word)
    flash_card.itemconfig(current_title, text=lan_a_title)

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
                wrapped_word = textwrap.fill((words_dict[i]["lan_b"]), width=25)
                flash_card.itemconfig(current_word, text=wrapped_word)
                # flash_card.itemconfig(current_word, text=words_dict[i]["lan_b"])
                flash_card.itemconfig(current_word, fill="white",  font=("Arial", 32, "bold"))
            elif words_dict[i]["lan_b"] == word_on:
                flash_card.itemconfig(card, image=card_front)
                flash_card.itemconfig(current_title, text=lan_a_title, font=("Arial", 32, "italic"))
                flash_card.itemconfig(current_word, text=words_dict[i]["lan_a"])
                flash_card.itemconfig(current_word, fill="black",  font=("Arial", 75, "bold"))


    not_it_wrong = Button(text="Not it", image=not_it_resized, highlightthickness=0,
                          command=lambda: list_output(not_it_list))
    not_it_wrong.grid(row=2, column=0, )
    not_it_wrong.config(padx=25, pady=25)

    got_it_right = Button(text="Got it", image=got_it_resized, highlightthickness=0, command=got_it_button_f)
    got_it_right.grid(row=2, column=1, )
    got_it_right.config(padx=25, pady=25)

    wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=wrong_button_f)
    wrong_button.config(highlightthickness=0, highlightbackground=wrong_button.master.cget("background"))
    wrong_button.grid(row=4, column=0)
    wrong_button.config(padx=25, pady=25)
    flip_button = Button(image=flip_resize, highlightthickness=0, command=flip_card)
    flip_button.grid(row=4, column=1)
    flip_button.config(padx=25, pady=25)
    correct_button = Button(image=right_button_img, highlightthickness=0, command=pick_word)
    correct_button.grid(row=5, column=0, columnspan=2)
    correct_button.config(padx=25, pady=25)


window.mainloop()
