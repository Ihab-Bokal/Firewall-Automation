import re
from FG_CLI_send_config import FirewallManager


class FirewallIPSearcher:
    def __init__(self, firewall_ip, username, password):
        self.fw_manager = FirewallManager(firewall_ip, username, password)
        self.fw_manager.connect()
        self.ip_pattern = re.compile(r"edit (.+)")

    def search_ip(self, search_ip):
        match = False
        command = f"show firewall address | grep -f {search_ip}"
        output = self.fw_manager.command(command)

        ip_references = self.ip_pattern.finditer(output)

        for ip_reference in ip_references:
            print(ip_reference.group(1))
            match = True

        if not match:
            print("No match")


if __name__ == "__main__":
    searcher = FirewallIPSearcher("IP_ADDRESS_HERE", "username", "password")

    search = input("Enter the IP address you want to look for: ")
    searcher.search_ip(search)
