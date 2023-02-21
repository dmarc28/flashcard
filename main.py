import random
from tkinter import *
from tkinter.ttk import Combobox
import textwrap
import pandas

# create the window
window = Tk()
window.title("Flash card")
window.config(padx=20, pady=20)
window.config(bg="white")

# creating label and combobox for user to choose what language user wants to use
select_language_label = Label(text="Choose the language:", font=("Arial", 12))
select_language_label.config(bg="white", padx=25, pady=25)
select_language_label.grid(row=0, column=0, sticky="N")
select_language_combobox = Combobox(window, values=["Arabic", "French"])
select_language_combobox.grid(row=0, column=1, columnspan=1, sticky="")

# creating a canvas to display the words
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
mastered_button_icon = PhotoImage(file='icons/Mastered_list.png')
mastered_button_icon_resized = mastered_button_icon.subsample(2, 2)
review_button_icon = PhotoImage(file="icons/Review_list.png")
review_button__resized = review_button_icon.subsample(2, 2)

# creating empty list to store the review list, mastered list and the displayed word
review_list = []
mastered_list = []
displayed_word = []


# this function takes the user choice from combobox and select which csv file to load
# this function also implement the rest of the App using a function "flashcard_run"
# flashcard function takes 3 inputs: csv_file, title for the selected language, and title for the known
# language (english)

def get_data():
    value = select_language_combobox.get()
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


# lan_a (lan - language) = is the column in csv file: selected language
# lan_b = known language, generally english

def flashcard_run(file, lan_a_title, lan_b_title):
    # when this function runs the first word is displayed here
    data = pandas.read_csv(file)
    words_dict = data.to_dict(orient="records")
    lan_a_title = lan_a_title
    lan_b_title = lan_b_title
    first_word = words_dict[random.randint(0, 15)]["lan_a"]
    print(first_word)
    flash_card.itemconfig(current_word, fill="black", font=("Arial", 75, "bold"))
    flash_card.itemconfig(current_word, text=first_word)
    flash_card.itemconfig(current_title, text=lan_a_title)

    # this function picks word and displays in the canvas
    def pick_word():
        word = random.choice(words_dict)
        if word in displayed_word:
            word = random.choice(words_dict)
        flash_card.itemconfig(card, image=card_front)
        flash_card.itemconfig(current_word, fill="black", font=("Arial", 75, "bold"))
        flash_card.itemconfig(current_word, text=(word['lan_a']))
        flash_card.itemconfig(current_title, text=lan_a_title)
        displayed_word.append(word)

    def add_to_review():
        word_on = flash_card.itemcget(current_word, 'text')
        for i in range(len(words_dict)):
            if words_dict[i]["lan_a"] == word_on or words_dict[i]["lan_b"] == word_on:
                review_list.append(words_dict[i])
                flash_card.itemconfig(current_word, fill="#EB455F")

    def add_to_mastered():
        for word in displayed_word:
            if word not in review_list and word not in mastered_list:
                mastered_list.append(word)
        list_generator(mastered_list)

    def list_generator(input_list):
        global pop
        pop = Toplevel(window)
        row_height = 50
        pop.geometry(f"700x{len(input_list) * row_height}")
        row = 0
        line_number = 1
        for item in input_list:
            output = (f"{line_number}: {(item['lan_a'])} : {(item['lan_b'])}")
            pop_label = Label(pop, text=str(output), font=("Arial", 22, "normal"), wraplength=500)
            pop_label.grid(row=row, column=0, sticky='w')
            row += 1
            line_number += 1

    def flip_card():
        word_on = flash_card.itemcget(current_word, 'text')

        for i in range(len(words_dict)):
            if words_dict[i]["lan_a"] == word_on:
                flash_card.itemconfig(card, image=card_back)
                flash_card.itemconfig(current_title, text=lan_b_title, font=("Arial", 32, "italic"))
                wrapped_word = textwrap.fill((words_dict[i]["lan_b"]), width=25)
                flash_card.itemconfig(current_word, text=wrapped_word)
                flash_card.itemconfig(current_word, fill="white", font=("Arial", 32, "bold"))
            elif words_dict[i]["lan_b"] == word_on:
                flash_card.itemconfig(card, image=card_front)
                flash_card.itemconfig(current_title, text=lan_a_title, font=("Arial", 32, "italic"))
                flash_card.itemconfig(current_word, text=words_dict[i]["lan_a"])
                flash_card.itemconfig(current_word, fill="black", font=("Arial", 75, "bold"))

    # creating other buttons

    review_button = Button(text="Not it", image=review_button__resized, highlightthickness=0,
                           command=lambda: list_generator(review_list))
    review_button.grid(row=2, column=0, )
    review_button.config(padx=25, pady=25)

    mastered_button = Button(text="Got it", image=mastered_button_icon_resized, highlightthickness=0, command=add_to_mastered)
    mastered_button.grid(row=2, column=1, )
    mastered_button.config(padx=25, pady=25)

    wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=add_to_review)
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
