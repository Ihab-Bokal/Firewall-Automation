import tkinter as tk
from CreateAddress import CreateAddress
from FirewallCommunicationBackend import FG_CLI_send_config


def set_active_firewall_policy():
    # Function to handle setting a firewall policy as active
    print("Redirect to Set Active Firewall Policy Page")


def select_firewall_policy():
    # Function to handle selecting firewall policies
    print("Redirect to Select Firewall Policies Page")


def get_addresses_csv():
    # Function to handle getting a CSV of addresses
    print("Redirect to Get Addresses CSV Page")


def create_service():
    # Function to handle creating a service
    print("Redirect to Create Service Page")


def get_services_csv():
    # Function to handle getting a CSV of services
    print("Redirect to Get Services CSV Page")


def create_firewall_policy():
    # Function to handle creating a firewall policy
    print("Redirect to Create Firewall Policy Page")


class HomePage:
    def __init__(self, root, fw_manager):
        self.root = root
        self.root.title("Firewall Management Main Page")
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        self.fw_manager = fw_manager

    def open_window(self):
        btn_create_address = tk.Button(self.frame, text="Create Address", command=self.create_address)
        btn_create_address.grid(row=0, column=0, pady=10)

        btn_get_addresses_csv = tk.Button(self.frame, text="Get Addresses CSV", command=get_addresses_csv)
        btn_get_addresses_csv.grid(row=1, column=0, pady=10)

        btn_create_service = tk.Button(self.frame, text="Create Service", command=create_service)
        btn_create_service.grid(row=2, column=0, pady=10)

        btn_get_services_csv = tk.Button(self.frame, text="Get Services CSV", command=get_services_csv)
        btn_get_services_csv.grid(row=3, column=0, pady=10)

        btn_create_firewall_policy = tk.Button(self.frame, text="Create Firewall Policy", command=create_firewall_policy)
        btn_create_firewall_policy.grid(row=4, column=0, pady=10)

        btn_select_firewall_policy = tk.Button(self.frame, text="Select Firewall Policies", command=select_firewall_policy)
        btn_select_firewall_policy.grid(row=5, column=0, pady=10)

        btn_set_active_firewall_policy = tk.Button(self.frame, text="Set Active Firewall Policy", command=set_active_firewall_policy)
        btn_set_active_firewall_policy.grid(row=6, column=0, pady=10)

    def create_address(self):
        self.frame.destroy()
        create_address_page = CreateAddress(self.root, self.fw_manager)
        create_address_page.open_window()


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    # fw_manager_inst.connect()

    app = HomePage(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
