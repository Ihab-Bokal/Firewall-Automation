import os
import tkinter as tk
import logging
from tkinter import messagebox, filedialog, ttk
from FirewallCommunicationBackend import FG_CLI_send_config
from CreateAddress import CreateAddress
from CreateService import CreateService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("../logs/firewall_manager.log"), logging.StreamHandler()]
)


class CreateFirewallPolicy:
    def __init__(self, root, fw_manager):
        self.entry_policy_name = None
        logging.info("Initializing CreateFirewallPolicy class")
        self.entry_dst = None
        self.entry_src = None
        self.entry_service = None
        self.incoming_interface = None
        self.outgoing_interface = None
        self.schedule = None
        self.action = None
        self.inspection_mode = None
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        logging.info("CreateFirewallPolicy UI frame initialized")

    def open_window(self):
        logging.info("Opening CreateFirewallPolicy window")
        button_width = 23

        label_policy_name = tk.Label(self.frame, text="Firewall Policy Name:")
        label_policy_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_policy_name = tk.Entry(self.frame, width=23)
        self.entry_policy_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        logging.info("Firewall Policy Name entry created")

        label_src = tk.Label(self.frame, text="Source Address Name:")
        label_src.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_src = tk.Entry(self.frame, width=23)
        self.entry_src.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        add_address_src = tk.Button(self.frame, text="+", command=self.open_create_addr)
        add_address_src.grid(row=1, column=2, padx=10, pady=10)
        logging.info("Source Address entry and button created")

        get_all_addresses = tk.Button(self.frame, text="Download Addresses", command=self.download_addresses,
                                      width=button_width)
        get_all_addresses.grid(row=1, column=3, padx=10, pady=10)
        logging.info("Download Addresses button created")

        label_dst = tk.Label(self.frame, text="Destination Address Name:")
        label_dst.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_dst = tk.Entry(self.frame, width=23)
        self.entry_dst.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        add_another_address_src = tk.Button(self.frame, text="+", command=self.open_create_addr)
        add_another_address_src.grid(row=2, column=2, padx=10, pady=10)
        logging.info("Destination Address entry and button created")

        label_service = tk.Label(self.frame, text="Service:")
        label_service.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_service = tk.Entry(self.frame, width=23)
        self.entry_service.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        add_service_src = tk.Button(self.frame, text="+", command=self.open_create_service)
        add_service_src.grid(row=3, column=2, padx=10, pady=10)
        logging.info("Service entry and button created")

        get_all_services = tk.Button(self.frame, text="Download Services", command=self.download_services,
                                     width=button_width)
        get_all_services.grid(row=3, column=3, padx=10, pady=10)
        logging.info("Download Services button created")

        label_incoming = tk.Label(self.frame, text="Incoming Interface:")
        label_incoming.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.incoming_interface = ttk.Combobox(self.frame, values=["lan", "wan"])
        self.incoming_interface.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        label_outgoing = tk.Label(self.frame, text="Outgoing Interface:")
        label_outgoing.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.outgoing_interface = ttk.Combobox(self.frame, values=["lan", "wan", "all"])
        self.outgoing_interface.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        label_schedule = tk.Label(self.frame, text="Schedule:")
        label_schedule.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.schedule = ttk.Combobox(self.frame, values=["always", "default-darrp-optimize", "none"])
        self.schedule.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        label_action = tk.Label(self.frame, text="Action:")
        label_action.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.action = ttk.Combobox(self.frame, values=["accept", "deny"])
        self.action.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        label_inspection = tk.Label(self.frame, text="Inspection Mode:")
        label_inspection.grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.inspection_mode = ttk.Combobox(self.frame, values=["Flow-based", "Proxy-based"])
        self.inspection_mode.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        submit_button = tk.Button(self.frame, text="Add Firewall Policy", command=self.add_firewall_policy, width=20)
        submit_button.grid(row=9, columnspan=4, pady=20)
        logging.info("Add Firewall Policy button created")

        go_back_button = tk.Button(self.frame, text="Back to Homepage", command=self.back, width=20)
        go_back_button.grid(row=10, columnspan=4, pady=10)
        logging.info("Back to Homepage button created")

    def open_create_addr(self):
        logging.info("Navigating to Create Address page")
        self.frame.destroy()
        create_addr_page = CreateAddress(self.root, self.fw_manager)
        create_addr_page.open_window()

    def open_create_service(self):
        logging.info("Navigating to Create Service page")
        self.frame.destroy()
        create_service_page = CreateService(self.root, self.fw_manager)
        create_service_page.open_window()

    def download_addresses(self):
        logging.info("Attempting to retrieve and save all addresses")
        if self.fw_manager:
            config_commands = ["show firewall address"]

            try:
                output = self.fw_manager.config(config_commands)

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
                    logging.info(f"TXT file saved successfully at {file_path}")
                else:
                    messagebox.showwarning("Cancelled", "Save operation cancelled.")
                    logging.warning("Save operation cancelled by user.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve addresses: {e}")
                logging.error(f"Failed to retrieve addresses: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")
            logging.error("Firewall manager is not connected.")

    def download_services(self):
        logging.info("Attempting to retrieve and save all services")
        if self.fw_manager:
            config_commands = ["show firewall service custom"]

            try:
                output = self.fw_manager.config(config_commands)

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
                    logging.info(f"TXT file saved successfully at {file_path}")
                else:
                    messagebox.showwarning("Cancelled", "Save operation cancelled.")
                    logging.warning("Save operation cancelled by user.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve services: {e}")
                logging.error(f"Failed to retrieve services: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")
            logging.error("Firewall manager is not connected.")

    def back(self):
        logging.info("Navigating back to homepage")
        self.frame.destroy()
        from Homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()

    def add_firewall_policy(self):
        logging.info("Adding firewall policy")

        policy_name = self.entry_policy_name.get()
        src_address = self.entry_src.get()
        dst_address = self.entry_dst.get()
        service = self.entry_service.get()
        incoming_iface = self.incoming_interface.get()
        outgoing_iface = self.outgoing_interface.get()
        schedule = self.schedule.get()
        action = self.action.get()
        inspection_mode = self.inspection_mode.get()

        if policy_name and src_address and dst_address and service:
            config_commands = [
                "config firewall policy",
                "edit 0",
                f"set name {policy_name}",
                f"set srcaddr {src_address}",
                f"set dstaddr {dst_address}",
                f"set service {service}",
                f"set srcintf {incoming_iface}",
                f"set dstintf {outgoing_iface}",
                f"set schedule {schedule}",
                f"set action {action}",
                f"set inspection-mode {inspection_mode}",
                "set logtraffic all",
                "next",
                "end"
            ]
            try:
                self.fw_manager.config(config_commands)
                messagebox.showinfo("Success", "Firewall policy added successfully.")
                logging.info("Firewall policy added successfully")
                self.entry_policy_name.delete(0, tk.END)
                self.entry_dst.delete(0, tk.END)
                self.entry_src.delete(0, tk.END)
                self.entry_service.delete(0, tk.END)
                self.incoming_interface.set("")
                self.outgoing_interface.set("")
                self.action.set("")
                self.inspection_mode.set("")
                self.schedule.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add firewall policy: {e}")
                logging.error(f"Failed to add firewall policy: {e}")
        else:
            messagebox.showerror("Error", "Please enter all required fields.")
            logging.warning("Attempt to add firewall policy without entering all required fields")


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager_inst.connect()

    app = CreateFirewallPolicy(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
