from cryptography.fernet import Fernet
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import os


def application_startup():
    generate_key()  # This will generate a key if one does not exist

def generate_key():
    key_file = "secret.key"
    # Check if the key file already exists
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        print("New encryption key generated.")
    else:
        print("Encryption key already exists.")

# Uncomment the below line to generate the key the first time you run the program
# generate_key()
def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    return Fernet(key).encrypt(message.encode())

def decrypt_message(encrypted_message):
    key = load_key()
    return Fernet(key).decrypt(encrypted_message).decode()

def create_table():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (service TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_account(service, username, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", (service, username, encrypt_message(password)))
    conn.commit()
    conn.close()

def get_account(service):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT username, password FROM accounts WHERE service=?", (service,))
    account_info = c.fetchone()
    conn.close()
    if account_info:
        return account_info[0], decrypt_message(account_info[1])
    else:
        return None

# Initialize the database table
create_table()

def add_account_gui():
    service = simpledialog.askstring("Service", "Enter the service name:")
    username = simpledialog.askstring("Username", "Enter the username:")
    password = simpledialog.askstring("Password", "Enter the password:")
    add_account(service, username, password)
    messagebox.showinfo("Success", "Successfully added the account!")

def get_account_gui():
    service = simpledialog.askstring("Retrieve", "Enter the service name:")
    account_info = get_account(service)
    if account_info:
        messagebox.showinfo("Account Info", f"Username: {account_info[0]}\nPassword: {account_info[1]}")
    else:
        messagebox.showinfo("Failed", "Account not found.")

def show_main_window():
    main_window = tk.Tk()
    main_window.title("This password app")
    main_window.mainloop()

def main():
    application_startup()
    # show_main_window()

    root = tk.Tk()
    root.title("Password Manager")

    add_button = tk.Button(root, text="Add Account", command=add_account_gui)
    add_button.pack(pady=5)

    get_button = tk.Button(root, text="Get Account Info", command=get_account_gui)
    get_button.pack(pady=5)

    root.mainloop()
if __name__ == "__main__":
    main()