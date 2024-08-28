import tkinter as tk
from tkinter import messagebox
from FirewallCommunicationBackend import FG_CLI_send_config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("../logs/firewall_manager.log"), logging.StreamHandler()]
)


class CreateAddress:
    def __init__(self, root, fw_manager):
        self.entry_ip = None
        self.entry_name = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        self.logger = logging.getLogger(__name__)  # Create a logger object

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
        self.logger.info("Navigating back to homepage.")  # Log navigation action
        self.frame.destroy()
        from Homepage import HomePage
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
                self.logger.info(f"Address '{name}' with IP '{ip_address}' added successfully.")  # Log success
                messagebox.showinfo("Success", "Address added to the firewall.")
            except Exception as e:
                self.logger.error(f"Failed to add address '{name}' with IP '{ip_address}': {e}")  # Log error
                messagebox.showerror("Error", f"Failed to add address: {e}")
        else:
            self.logger.warning("Attempted to add address with missing IP Address or Name.")  # Log warning
            messagebox.showerror("Error", "Please enter both IP Address and Name.")


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    # fw_manager.connect()

    app = CreateAddress(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
