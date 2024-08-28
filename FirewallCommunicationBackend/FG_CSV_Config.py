from csv import DictReader
from FG_CLI_send_config import FirewallManager


class FirewallConfigurator:
    def __init__(self, csv_file_path, firewall_ip, username, password):
        self.ip_details = None
        self.csv_file_path = csv_file_path
        self.fw_manager = FirewallManager(firewall_ip, username, password)
        self.fw_manager.connect()

    def load_ip_details(self):
        with open(self.csv_file_path, encoding='utf-8-sig') as csv_users:
            self.ip_details = list(DictReader(csv_users))

    def configure_firewall(self):
        for ip in self.ip_details:
            print(f"{'#'*20} Configuring Object {ip['Name']} {'#'*20}")
            config = [
                "config firewall address",
                f"edit {ip['Name']}",
                "set type ipmask",
                f"set subnet {ip['IP']}",
                "end"
            ]
            sent_config = self.fw_manager.config(config)
            print(sent_config)


if __name__ == "__main__":
    configurator = FirewallConfigurator("../Test files/users.csv", "IP_ADDRESS_HERE", "username", "password")
    configurator.load_ip_details()
    configurator.configure_firewall()
