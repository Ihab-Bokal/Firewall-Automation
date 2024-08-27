import os
import tkinter as tk
from tkinter import messagebox, filedialog
from FirewallCommunicationBackend import FG_CLI_send_config
from CreateAddress import CreateAddress
from CreateService import CreateService


class CreateFirewallPolicy:
    def __init__(self, root, fw_manager):
        self.entry_dst = None
        self.entry_src = None
        self.entry_service = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)

    def open_window(self):
        button_width = 23

        label_src = tk.Label(self.frame, text="Source Address:")
        label_src.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_src = tk.Entry(self.frame)
        self.entry_src.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        add_address_src = tk.Button(self.frame, text="+", command=self.open_create_addr)
        add_address_src.grid(row=0, column=2, padx=10, pady=10)
        get_all_addresses = tk.Button(self.frame, text="download addresses", command=self.download_addresses, width=button_width)
        get_all_addresses.grid(row=0, column=3, padx=10, pady=10)

        label_dst = tk.Label(self.frame, text="Destination Address:")
        label_dst.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_dst = tk.Entry(self.frame)
        self.entry_dst.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        add_another_address_src = tk.Button(self.frame, text="+", command=self.open_create_addr)
        add_another_address_src.grid(row=1,  column=2, padx=10, pady=10)

        label_service = tk.Label(self.frame, text="Service:")
        label_service.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_service = tk.Entry(self.frame)
        self.entry_service.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        add_service_src = tk.Button(self.frame, text="+", command=self.open_create_service)
        add_service_src.grid(row=2, column=2, padx=10, pady=10)
        get_all_addresses = tk.Button(self.frame, text="download services", command=self.download_services, width=button_width)
        get_all_addresses.grid(row=2, column=3, padx=10, pady=10)

        submit_button = tk.Button(self.frame, text="Add Firewall Policy", command=self.add_firewall_policy, width=20)
        submit_button.grid(row=3, columnspan=4, pady=20)

        go_back_button = tk.Button(self.frame, text="Back to homepage", command=self.back, width=20)
        go_back_button.grid(row=4, columnspan=4, pady=10)

    def open_create_addr(self):
        self.frame.destroy()
        create_addr_page = CreateAddress(self.root, self.fw_manager)
        create_addr_page.open_window()

    def open_create_service(self):
        self.frame.destroy()
        create_addr_page = CreateService(self.root, self.fw_manager)
        create_addr_page.open_window()

    def download_addresses(self):
        if self.fw_manager:
            config_commands = ["show firewall address"]

            try:
                output = self.fw_manager.command(config_commands)    # MODIFICATION

                if output is None:
                    raise ValueError("No data received from the firewall.")

                file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt"),
                                                                    ("All files", "*.*")])
                if file_path:
                    with open(file_path, mode='w') as file:
                        for line in output:
                            file.write(line + os.linesep)

                    messagebox.showinfo("Success", f"TXT file saved successfully at {file_path}.")
                else:
                    messagebox.showwarning("Cancelled", "Save operation cancelled.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve addresses: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")

    def download_services(self):
        if self.fw_manager:
            config_commands = ["show firewall service custom"]

            try:
                output = self.fw_manager.command(config_commands)

                if output is None:
                    raise ValueError("No data received from the firewall.")

                file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt"),
                                                                    ("All files", "*.*")])
                if file_path:
                    with open(file_path, mode='w') as file:
                        if isinstance(output, str):
                            file.write(output)
                        else:
                            for line in output:
                                file.write(line + os.linesep)

                    messagebox.showinfo("Success", f"TXT file saved successfully at {file_path}.")
                else:
                    messagebox.showwarning("Cancelled", "Save operation cancelled.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve services: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")

    def back(self):
        self.frame.destroy()
        from homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()

    def add_firewall_policy(self):
        src_address = self.entry_src.get()
        dst_address = self.entry_dst.get()
        service = self.entry_service.get()

        if src_address and dst_address and service:
            config_commands = [
                "config firewall policy",
                "edit 0",
                f"set srcaddr {src_address}",
                f"set dstaddr {dst_address}",
                f"set service {service}",
                "set action accept",
                "set schedule always",
                "set logtraffic all",
                "next",
                "end"
            ]
            try:
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Firewall policy added successfully. Note that schedule is set to always in this app version")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add firewall policy: {e}")
        else:
            messagebox.showerror("Error", "Please enter all required fields.")


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    # fw_manager.connect()

    app = CreateFirewallPolicy(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
