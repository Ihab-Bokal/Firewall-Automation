import tkinter as tk
from tkinter import messagebox
from FirewallCommunicationBackend import FG_CLI_send_config


class CreateService:
    def __init__(self, root, fw_manager):
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)

    def open_window(self):
        self.label_name = tk.Label(self.frame, text="Service Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_protocol = tk.Label(self.frame, text="Protocol:")
        self.label_protocol.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_protocol = tk.Entry(self.frame)
        self.entry_protocol.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_port_range = tk.Label(self.frame, text="Port Range:")
        self.label_port_range.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_port_range = tk.Entry(self.frame)
        self.entry_port_range.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.submit_button = tk.Button(self.frame, text="Add Service", command=self.add_service)
        self.submit_button.grid(row=3, columnspan=2, pady=20)

        self.go_back_button = tk.Button(self.frame, text="Back to homepage", command=self.back)
        self.go_back_button.grid(row=4, columnspan=2, pady=10)

    def back(self):
        self.frame.destroy()
        from homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()

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
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Service added to the firewall.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add service: {e}")
        else:
            messagebox.showerror("Error", "Please enter Service Name, Protocol, and Port Range.")


if __name__ == "__main__":
    root = tk.Tk()
    fw_manager = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    # fw_manager.connect()

    app = CreateService(root, fw_manager)
    app.open_window()
    root.mainloop()
