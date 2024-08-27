import sqlite3
import tkinter as tk
from tkinter import messagebox
from homepage import HomePage
from FirewallConnect import FirewallConnect


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(pady=50)

        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.grid(row=0, column=0, sticky="e")
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1)

        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.grid(row=2, column=0, sticky="e", pady=10)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=2, column=1, pady=10)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, pady=30)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND passphrase = ?", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login", "Login successful!")
            self.frame.destroy()
            home = HomePage(self.root, None)
            home.open_window()
            # fwConn = FirewallConnect(self.root)
            # fwConn.open_window()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

        conn.close()


if __name__ == "__main__":
    root_inst = tk.Tk()
    app = LoginApp(root_inst)
    root_inst.mainloop()
