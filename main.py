from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

BLUE = "#A6D0DD"
RED = "#850000"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pw_generator():
    pw_entry.delete(0, 'end')
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    password_no = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_no + password_symbol + password_letter

    random.shuffle(password_list)
    new_password = ''.join(password_list)
    pw_entry.insert(0, new_password)
    pyperclip.copy(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pw():
    input_web = web_entry.get()
    input_email = Email_entry.get()
    input_pw = pw_entry.get()

    new_data = {
        input_web: {
            "Email": input_email,
            "Password": input_pw,
        }
    }

    if len(input_web) == 0 or len(input_pw) == 0:
        messagebox.showinfo(title="OOPS!", message="Please don't leave any field empty!")

    else:
        try:
            with (open("SavedData.json", mode="r") as data_file):
                # json.dump(new_data, data_file, indent=4)
                # read data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("SavedData.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # add new data
            data.update(new_data)
            with open("SavedData.json", mode="w") as data_file:
                # adding data in dict
                json.dump(data, data_file, indent=4)
        finally:
            pw_entry.delete(0, 'end')
            web_entry.delete(0, 'end')


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_pw():
    input_web = web_entry.get().capitalize()
    try:
        with open("SavedData.json", "r") as data_file:
            data = json.load(data_file)
        input_data = data[input_web]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data Not Found")
    except KeyError:
        messagebox.showinfo(title="Oops!", message=f"No details for {input_web} exists.")
    else:
        email_data = input_data["Email"]
        pw_data = input_data["Password"]
        messagebox.showinfo(title=input_web, message=f"Email: {email_data}\nPassword: {pw_data}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("The Password Manager")
window.config(padx=30, pady=30, bg=BLUE)

canvas = Canvas(width=300, height=300, bg=BLUE, highlightthickness=0)
lock = PhotoImage(file="logo.png")
canvas.create_image(150, 150, image=lock)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website: ", font="Helvetica", fg=RED, bg=BLUE)
website.grid(column=0, row=1)

Email = Label(text="Email/UserID: ", font="Helvetica", fg=RED, bg=BLUE)
Email.grid(column=0, row=2)

pw = Label(text="Password: ", font="Helvetica", fg=RED, bg=BLUE)
pw.grid(column=0, row=3)

# TextBox
web_entry = Entry(width=40)
web_entry.grid(column=1, row=1, padx=5, pady=5)
web_entry.focus()

Email_entry = Entry(width=58)
Email_entry.insert(END, "mariyachikhly84@gmail.com")
Email_entry.grid(column=1, row=2, columnspan=2, padx=5, pady=5)

pw_entry = Entry(width=40)
pw_entry.grid(column=1, row=3)

# Buttons
generate_pw = Button(text="Generate Password", bd=1, command=pw_generator)
generate_pw.grid(column=2, row=3)

add = Button(text="ADD", width=58, bd=1, command=save_pw)
add.grid(column=1, row=4, columnspan=2, padx=5, pady=5)

search = Button(text="Search", width=16, bd=1, command=search_pw)
search.grid(column=2, row=1)

window.mainloop()
