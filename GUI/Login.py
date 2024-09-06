import sqlite3
import tkinter as tk
import logging
from tkinter import messagebox
from .FirewallConnect import FirewallConnect

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("./logs/firewall_manager.log"), logging.StreamHandler()]
)


class Login:
    def __init__(self, root):
        logging.info("Initializing Login class")
        self.root = root
        self.root.title("Login Page")
        logging.info("Login window created")

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(pady=50)
        logging.info("Frame for login UI elements initialized")

        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.grid(row=0, column=0, sticky="e")
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1)
        logging.info("Username entry field created")

        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.grid(row=2, column=0, sticky="e", pady=10)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=2, column=1, pady=10)
        logging.info("Password entry field created")

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, pady=30)
        logging.info("Login button created")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        logging.info(f"Login attempt with username: {username}")

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        logging.info("Connected to the SQLite database")

        cursor.execute("SELECT * FROM users WHERE username = ? AND passphrase = ?", (username, password))
        result = cursor.fetchone()

        if result:
            logging.info(f"Login successful for user: {username}")
            messagebox.showinfo("Login", "Login successful!")
            self.frame.destroy()
            fwConn = FirewallConnect(self.root)
            fwConn.open_window()
        else:
            logging.warning(f"Login failed for user: {username}")
            messagebox.showerror("Login", "Invalid username or password.")

        conn.close()
        logging.info("SQLite database connection closed")


if __name__ == "__main__":
    logging.info("Starting Login application")
    root_inst = tk.Tk()
    app = Login(root_inst)
    root_inst.mainloop()
    logging.info("Login application terminated")
