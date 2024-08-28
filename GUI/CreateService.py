import tkinter as tk
from tkinter import messagebox
import logging
from FirewallCommunicationBackend import FG_CLI_send_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("../logs/firewall_manager.log"), logging.StreamHandler()]
)


class CreateService:
    def __init__(self, root, fw_manager):
        self.entry_port_range = None
        self.entry_protocol = None
        self.entry_name = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        logging.debug("CreateService initialized.")

    def open_window(self):
        button_width = 20

        label_name = tk.Label(self.frame, text="Service Name:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_protocol = tk.Label(self.frame, text="Protocol:")
        label_protocol.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_protocol = tk.Entry(self.frame)
        self.entry_protocol.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        label_port_range = tk.Label(self.frame, text="Port Range:")
        label_port_range.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_port_range = tk.Entry(self.frame)
        self.entry_port_range.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        submit_button = tk.Button(self.frame, text="Add Service", command=self.add_service, width=button_width)
        submit_button.grid(row=3, columnspan=2, pady=20)

        go_back_button = tk.Button(self.frame, text="Back to homepage", command=self.back, width=button_width)
        go_back_button.grid(row=4, columnspan=2, pady=10)

        logging.debug("CreateService window opened.")

    def back(self):
        self.frame.destroy()
        from Homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()
        logging.debug("Back to homepage.")

    def add_service(self):
        service_name = self.entry_name.get()
        protocol = self.entry_protocol.get()
        port_range = self.entry_port_range.get()

        if service_name and protocol and port_range:
            config_commands = [
                "config firewall service custom",
                f"edit {service_name}",
                f"set protocol {protocol.lower()}",
                f"set {protocol.lower()}-portrange {port_range}",
                "next",
                "end"
            ]
            try:
                logging.info(f"Adding service with commands: {config_commands}")
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Service added to the firewall.")
                logging.info("Service added successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add service: {e}")
                logging.error(f"Failed to add service: {e}")
        else:
            messagebox.showerror("Error", "Please enter Service Name, Protocol, and Port Range.")
            logging.warning("Add service failed due to missing fields.")


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager_inst.connect()

    app = CreateService(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
