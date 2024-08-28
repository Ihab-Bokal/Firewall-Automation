import tkinter as tk
import logging
import csv
import os
from tkinter import filedialog, messagebox
from CreateAddress import CreateAddress
from FirewallCommunicationBackend import FG_CLI_send_config
from CreateService import CreateService
from CreateFirewallPolicy import CreateFirewallPolicy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("../logs/firewall_manager.log"), logging.StreamHandler()]
)


def set_active_firewall_policy():
    logging.info("Redirecting to Set Active Firewall Policy Page")
    print("Redirect to Set Active Firewall Policy Page")


def generate_addresses_csv(addresses):
    if addresses:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv"),
                                                                ("All files", "*.*")])
            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "IP Address"])
                    writer.writeheader()
                    writer.writerows(addresses)

                messagebox.showinfo("Success", f"CSV file saved successfully at {file_path}.")
                logging.info(f"CSV file saved successfully at {file_path}")
            else:
                messagebox.showwarning("Cancelled", "Save operation cancelled.")
                logging.warning("Save operation cancelled by user.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {e}")
            logging.error(f"Failed to save CSV file: {e}")
    else:
        messagebox.showwarning("No Data", "No address data available to save.")
        logging.warning("No address data available to save.")


class HomePage:
    def __init__(self, root, fw_manager):
        logging.info("Initializing HomePage class")
        self.root = root
        self.root.title("Firewall Management Main Page")
        logging.info("Main window title set")

        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        self.fw_manager = fw_manager
        logging.info("HomePage UI frame initialized")

    def open_window(self):
        logging.info("Opening HomePage window")
        button_width = 25

        btn_create_address = tk.Button(self.frame, text="Create Address", command=self.create_address,
                                       width=button_width)
        btn_create_address.grid(row=0, column=0, pady=10)
        logging.info("Create Address button created")

        btn_get_addresses_csv = tk.Button(self.frame, text="Get all Addresses", command=self.get_all_addresses,
                                          width=button_width)
        btn_get_addresses_csv.grid(row=1, column=0, pady=10)
        logging.info("Get all Addresses button created")

        btn_create_service = tk.Button(self.frame, text="Create Service", command=self.create_service,
                                       width=button_width)
        btn_create_service.grid(row=2, column=0, pady=10)
        logging.info("Create Service button created")

        btn_get_services_csv = tk.Button(self.frame, text="Get all Services", command=self.get_all_services,
                                         width=button_width)
        btn_get_services_csv.grid(row=3, column=0, pady=10)
        logging.info("Get all Services button created")

        btn_create_firewall_policy = tk.Button(self.frame, text="Create Firewall Policy",
                                               command=self.create_firewall_policy, width=button_width)
        btn_create_firewall_policy.grid(row=4, column=0, pady=10)
        logging.info("Create Firewall Policy button created")

        btn_select_firewall_policy = tk.Button(self.frame, text="Get all Firewall Policies",
                                               command=self.get_all_fw_policies, width=button_width)
        btn_select_firewall_policy.grid(row=5, column=0, pady=10)
        logging.info("Get all Firewall Policies button created")

        btn_set_active_firewall_policy = tk.Button(self.frame, text="Set Active Firewall Policy",
                                                   command=set_active_firewall_policy, width=button_width)
        btn_set_active_firewall_policy.grid(row=6, column=0, pady=10)
        logging.info("Set Active Firewall Policy button created")

    def create_address(self):
        logging.info("Navigating to Create Address page")
        self.frame.destroy()
        create_address_page = CreateAddress(self.root, self.fw_manager)
        create_address_page.open_window()

    def get_all_fw_policies(self):
        logging.info("Attempting to retrieve all firewall policies")
        if self.fw_manager:
            config_commands = ["show firewall policy"]

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
                messagebox.showerror("Error", f"Failed to retrieve firewall policies: {e}")
                logging.error(f"Failed to retrieve firewall policies: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")
            logging.error("Firewall manager is not connected.")

    def create_firewall_policy(self):
        logging.info("Navigating to Create Firewall Policy page")
        self.frame.destroy()
        create_fw_policy_page = CreateFirewallPolicy(self.root, self.fw_manager)
        create_fw_policy_page.open_window()

    def create_service(self):
        logging.info("Navigating to Create Service page")
        self.frame.destroy()
        create_service_page = CreateService(self.root, self.fw_manager)
        create_service_page.open_window()

    def get_all_services(self):
        logging.info("Attempting to retrieve all services")
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

    def get_all_addresses(self):
        logging.info("Attempting to retrieve all addresses")
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

    def get_addresses_csv(self):
        logging.info("Attempting to retrieve and save all addresses as CSV")
        addresses = self.fetch_addresses_from_firewall()
        generate_addresses_csv(addresses)

    def fetch_addresses_from_firewall(self):
        logging.info("Fetching addresses from firewall")
        if self.fw_manager:
            config_commands = ["show firewall address"]

            try:
                output = self.fw_manager.config(config_commands)

                addresses = []
                for line in output:
                    if "name=" in line and "subnet=" in line:
                        name = line.split("name=")[1].split(",")[0]
                        subnet = line.split("subnet=")[1].split(",")[0]
                        addresses.append({"Name": name, "IP Address": subnet})

                logging.info("Addresses successfully fetched from firewall")
                return addresses

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve addresses: {e}")
                logging.error(f"Failed to retrieve addresses: {e}")
                return None
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")
            logging.error("Firewall manager is not connected.")
            return None


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager_inst.connect()

    app = HomePage(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
