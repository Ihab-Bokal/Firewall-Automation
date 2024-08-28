import tkinter as tk
from tkinter import messagebox, ttk
import logging
from FirewallCommunicationBackend import FG_CLI_send_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("../logs/firewall_manager.log"), logging.StreamHandler()]
)


class CreateService:
    def __init__(self, root, fw_manager):
        self.entry_name = None
        self.protocol_combobox = None
        self.dest_protocol_combobox = None
        self.entry_low = None
        self.entry_high = None
        self.category_combobox = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        self.logger = logging.getLogger(__name__)

        self.protocols = [
            "TCP/UDP/SCTP",
            "IP",
            "ICMP"
        ]

        self.dest_protocols = [
            "TCP",
            "UDP",
            "SCTP"
        ]

        logging.debug("CreateService initialized.")

    def open_window(self):
        button_width = 20

        label_name = tk.Label(self.frame, text="Service Name:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_protocol = tk.Label(self.frame, text="Protocol:")
        label_protocol.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.protocol_combobox = ttk.Combobox(self.frame, values=self.protocols)
        self.protocol_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.protocol_combobox.set(self.protocols[0])

        label_dest_port = tk.Label(self.frame, text="Destination Port:")
        label_dest_port.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.dest_protocol_combobox = ttk.Combobox(self.frame, values=self.dest_protocols)
        self.dest_protocol_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.dest_protocol_combobox.set(self.dest_protocols[0])

        label_low = tk.Label(self.frame, text="Low:")
        label_low.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.entry_low = tk.Entry(self.frame, width=10)
        self.entry_low.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        label_high = tk.Label(self.frame, text="High:")
        label_high.grid(row=2, column=4, padx=10, pady=10, sticky="e")
        self.entry_high = tk.Entry(self.frame, width=10)
        self.entry_high.grid(row=2, column=5, padx=10, pady=10, sticky="w")

        label_category = tk.Label(self.frame, text="Category:")
        label_category.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.category_combobox = ttk.Combobox(self.frame, values=[
            "Authentication",
            "Email",
            "File Access",
            "General",
            "Network Services",
            "Remote Access",
            "Tunneling",
            "Uncategorized",
            "VoIP, Messaging & Other Applications",
            "Web Access",
            "Web Proxy"
        ])
        self.category_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.category_combobox.set("Authentication")

        submit_button = tk.Button(self.frame, text="Add Service", command=self.add_service, width=button_width)
        submit_button.grid(row=4, columnspan=6, pady=20)

        go_back_button = tk.Button(self.frame, text="Back to homepage", command=self.back, width=button_width)
        go_back_button.grid(row=5, columnspan=6, pady=10)

        logging.debug("CreateService window opened.")

    def back(self):
        self.frame.destroy()
        from Homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()
        logging.debug("Back to homepage.")

    def add_service(self):
        service_name = self.entry_name.get()
        protocol = self.protocol_combobox.get()
        dest_protocol = self.dest_protocol_combobox.get()
        low_port = self.entry_low.get()
        high_port = self.entry_high.get()
        category = self.category_combobox.get()

        if service_name and protocol and low_port and high_port:
            config_commands = [
                "config firewall service custom",
                f"edit {service_name}",
                f"set protocol {protocol.lower()}",
                f"set {dest_protocol.lower()}-portrange {low_port} {high_port}",
                f"set category {category}",
                "next",
                "end"
            ]
            try:
                self.logger.info(f"Adding service with commands: {config_commands}")
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Service added to the firewall.")
                self.logger.info("Service added successfully.")
                self.entry_low.delete(0, tk.END)
                self.entry_high.delete(0, tk.END)
                self.entry_name.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add service: {e}")
                self.logger.error(f"Failed to add service: {e}")
        else:
            messagebox.showerror("Error",
                                 "Please enter Service Name, Protocol, Destination Ports, and select a Category.")
            self.logger.warning("Add service failed due to missing fields.")


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager_inst.connect()

    app = CreateService(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
