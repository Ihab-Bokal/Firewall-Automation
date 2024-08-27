import tkinter as tk
from tkinter import messagebox
from FirewallCommunicationBackend import FG_CLI_send_config


class CreateAddress:
    def __init__(self, root, fw_manager):
        self.entry_ip = None
        self.entry_name = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)

    def open_window(self):
        button_width = 20
        
        label_ip = tk.Label(self.frame, text="IP Address:")
        label_ip.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_ip = tk.Entry(self.frame)
        self.entry_ip.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_name = tk.Label(self.frame, text="Name:")
        label_name.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        submit_button = tk.Button(self.frame, text="Add Address", command=self.add_address, width=button_width)
        submit_button.grid(row=2, columnspan=2, pady=20)

        go_back_button = tk.Button(self.frame, text="Back to homepage", command=self.back, width=button_width)
        go_back_button.grid(row=3, columnspan=2, pady=10)

    def back(self):
        self.frame.destroy()
        from homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()

    def add_address(self):
        ip_address = self.entry_ip.get()
        name = self.entry_name.get()

        if ip_address and name:
            config_commands = [
                "config firewall address",
                f"edit {name}",
                "set type ipmask",
                f"set subnet {ip_address}/32",
                "end"
            ]
            try:
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Address added to the firewall.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add address: {e}")
        else:
            messagebox.showerror("Error", "Please enter both IP Address and Name.")


if __name__ == "__main__":
    root = tk.Tk()
    fw_manager = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    # fw_manager.connect()

    app = CreateAddress(root, fw_manager)
    app.open_window()
    root.mainloop()
