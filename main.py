from tkinter import *
from tkinter import messagebox
# import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random


def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_name.insert(0, password)
    # pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_new():
    website_inp = website_name.get()
    email_inp = email_name.get()
    pass_inp = password_name.get()
    new_data = {
        website_inp.title(): {
            "email": email_inp,
            "password": pass_inp,
        }
    }

    if len(website_inp) == 0 or len(pass_inp) == 0:
        messagebox.showerror(title="Error", message="All the fields must be filled")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.JSONDecodeError:
            # print("JSON decode error.\nWriting new data.")
            data = new_data
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_name.delete(0, END)
            password_name.delete(0, END)


# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search():
    website_inp = website_name.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except json.JSONDecodeError:
        messagebox.showerror(title="File Empty", message="Please save some data first to search")
    else:
        try:
            email = data[website_inp]["email"]
            password = data[website_inp]["password"]
            messagebox.showinfo(title={website_inp}, message=f"Email : {email}\nPassword : {password}")
        except KeyError:
            messagebox.showerror(title="Error", message=f"{website_inp}'s details not available")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=40)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_name = Entry()
website_name.grid(column=1, row=1, sticky="EW")
website_name.focus()

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_name = Entry()
email_name.grid(column=1, row=2, columnspan=2, sticky="EW")
email_name.insert(END, "abc@xyz.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_name = Entry()
password_name.grid(column=1, row=3, sticky="EW")

generate_button = Button(text="Generate Password", command=generate)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", command=add_new)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
logo_canv = canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

window.mainloop()
