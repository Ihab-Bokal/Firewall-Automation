from netmiko import Netmiko


class FirewallManager:
    def __init__(self, host, username, password):
        self.device_params = {
            'host': host,
            'username': username,
            'password': password,
            'device_type': "fortinet"
        }
        self.connection = None

    def connect(self):
        print(f"{'#'*20} Connecting {'#'*20}")
        self.connection = Netmiko(**self.device_params)
        print(f"{'#'*20} Connected {'#'*20}")

    def config(self, config_commands):
        if self.connection:
            send_config = self.connection.send_config_set(config_commands)
            print(send_config)
        else:
            print("Not connected to the firewall. Please connect first.")


fw_manager = FirewallManager(host="FW_IP_ADDRESS", username="username", password="password")
fw_manager.connect()

config = [
    "config firewall address",
    "edit IP_101",
    "set type ipmask",
    "set subnet 192.168.0.101/32",
    "end"
]
fw_manager.config(config)
