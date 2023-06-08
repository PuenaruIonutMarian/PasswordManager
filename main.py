import json
from tkinter import *
from tkinter import messagebox  # message box for  pop ups
from random import randint, shuffle, choice
import pyperclip

BLUE = "#40DFEF"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)  # generates password on password row
    pyperclip.copy(password)  # to copy the generated string passwd


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # the first is canceling the error when datajson doesn't exists
            # the second one when there is no data in datajson

            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# -------------------------CLEAR---------------------------------------- #
def clear_data():
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
    with open("data.json", "w") as data_file:
        data.clear()
        json.dump(data, data_file, indent=4)




# ----------------------------- Search Function --------------------------------- #
def search_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
locker_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", bg="white")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)

# Buttons
generate_button = Button(text="Generate Password", bg=BLUE, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, bg=BLUE, command=save)
add_button.grid(column=1, row=4, columnspan=2)

clear_button = Button(text="Recycle", width=44, bg="white", command=clear_data)
clear_button.grid(column=1, row=5, columnspan=2)

search_button = Button(text="Search", width=14, bg="white", command=search_password)
search_button.grid(column=2, row=1)

# Inputs
website_entry = Entry(width=33, highlightthickness=1)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=52, highlightthickness=1)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "myemail@gmail.com")
# for the coursor after the mail instead of 0 put END
password_entry = Entry(width=33, highlightthickness=1)
password_entry.grid(column=1, row=3)

window.mainloop()
