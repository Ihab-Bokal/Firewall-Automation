import sqlite3
import tkinter as tk
from tkinter import messagebox


def login():
    username = entry_username.get()
    password = entry_password.get()

    # Example: Simple check
    if username == "admin" and password == "password":
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Page")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(pady=50)

    label_username = tk.Label(frame, text="Username:")
    label_username.grid(row=0, column=0, sticky="e")

    entry_username = tk.Entry(frame)
    entry_username.grid(row=0, column=1)

    label_password = tk.Label(frame, text="Password:")
    label_password.grid(row=2, column=0, sticky="e", pady=10)

    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=2, column=1, pady=10)

    login_button = tk.Button(frame, text="Login", command=login)
    login_button.grid(row=3, columnspan=2, pady=30)

    root.mainloop()

    # Create Table
    conn = sqlite3.connect('users.db')

    create_table = '''
    CREATE TABLE IF NOT EXISTS Allowed_users (username TEXT, password TEXT)
    '''

    conn.execute(create_table)


    conn.close()
