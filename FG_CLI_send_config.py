from netmiko import Netmiko


class FirewallManager:
    def __init__(self, host: str, username: str, password: str):
        # Add cisco
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

    # Command as in "Commander"
    def command(self, command: str):
        if self.connection:
            send_command = self.connection.send_command(command)
            return send_command
        else:
            print("Not connected to the firewall. Please connect first.")

    def config(self, config_commands: list[str]):
        if self.connection:
            send_config = self.connection.send_config_set(config_commands)
            print(send_config)
        else:
            print("Not connected to the firewall. Please connect first.")


if __name__ == "__main__":
    fw_manager = FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager.connect()

    config = [
        "config firewall address",
        "edit IP_101",
        "set type ipmask",
        "set subnet 192.168.0.101/32",
        "end"
    ]
    fw_manager.config(config)
