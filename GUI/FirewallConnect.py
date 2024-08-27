import tkinter as tk
from tkinter import messagebox
from FirewallCommunicationBackend import FG_CLI_send_config
from homepage import HomePage


class FirewallConnect:
    def __init__(self, root):
        self.root = root
        self.fw_manager = None

    def open_window(self):
        self.root.title("Connexion à la FortiGate")

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(pady=50)

        # Firewall IP address
        self.label_fw_ip = tk.Label(self.frame, text="Adresse IP du Firewall:")
        self.label_fw_ip.grid(row=0, column=0, sticky="e")
        self.entry_fw_ip = tk.Entry(self.frame)
        self.entry_fw_ip.grid(row=0, column=1)

        # Firewall username
        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.grid(row=1, column=0, sticky="e", pady=10)
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=1, column=1, pady=10)

        # Firewall password
        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.grid(row=2, column=0, sticky="e", pady=0)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=2, column=1, pady=0)

        # Connect button
        self.connect_button = tk.Button(self.frame, text="Connexion", command=self.connect)
        self.connect_button.grid(row=3, columnspan=2, pady=10)

    def connect(self):
        fw_ip = self.entry_fw_ip.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.fw_manager = FG_CLI_send_config.FirewallManager(host=fw_ip, username=username, password=password)
        try:
            self.fw_manager.connect()
            messagebox.showinfo("Connexion", "Connexion établie avec succès!")
            self.frame.destroy()
            home = HomePage(self.root, self.fw_manager)
            home.open_window()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {e}")

    def get_fw_manager(self):
        return self.fw_manager


if __name__ == "__main__":
    root_inst = tk.Tk()
    app = FirewallConnect(root_inst)
    app.open_window()
    root_inst.mainloop()
