import logging
from netmiko import Netmiko
from tkinter import messagebox

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/firewall_manager.log"),
        logging.StreamHandler()
    ]
)


class FirewallManager:
    def __init__(self, host: str, username: str, password: str):
        self.device_params = {
            'host': host,
            'username': username,
            'password': password,
            'device_type': "fortinet"
        }
        self.connection = None
        logging.info(f"FirewallManager initialized with host: {host}, username: {username}")

    def connect(self):
        try:
            logging.info(f"Attempting to connect to FortiGate at {self.device_params['host']} with username {self.device_params['username']}")
            self.connection = Netmiko(**self.device_params)
            logging.info("Successfully connected to FortiGate.")
        except Exception as e:
            logging.error(f"Failed to connect to FortiGate: {e}")
            messagebox.showerror("Error", f"Failed to connect to FortiGate: {e}")

    def command(self, command: str):
        if self.connection:
            try:
                logging.info(f"Sending command: {command}")
                send_command = self.connection.send_command(command)
                logging.info(f"Command response: {send_command}")
                return send_command.splitlines()
            except Exception as e:
                logging.error(f"Failed to send command '{command}': {e}")
                messagebox.showerror("Error", f"Failed to send command: {e}")
        else:
            logging.warning("Attempted to send command without an active connection.")
            messagebox.showerror("Error", "Not connected to the firewall. Please connect first.")

    def config(self, config_commands: list[str]):
        if self.connection:
            try:
                logging.info(f"Sending configuration commands: {config_commands}")
                send_config = self.connection.send_config_set(config_commands)
                logging.info(f"Configuration response: {send_config}")
                return send_config.splitlines()
            except Exception as e:
                logging.error(f"Failed to send configuration commands: {e}")
                messagebox.showerror("Error", f"Failed to send configuration commands: {e}")
        else:
            logging.warning("Attempted to send configuration without an active connection.")
            messagebox.showerror("Error", "Not connected to the firewall. Please connect first.")

    def disconnect(self):
        if self.connection:
            logging.info("Disconnecting from FortiGate.")
            self.connection.disconnect()
            logging.info("Successfully disconnected from FortiGate.")
        else:
            logging.warning("Attempted to disconnect without an active connection.")


# Example usage
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
    fw_manager.disconnect()
