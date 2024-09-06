import os
import tkinter as tk
import logging
from tkinter import messagebox, filedialog
from datetime import datetime
from FirewallCommunicationBackend import FG_CLI_send_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("./logs/firewall_log_retriever.log"), logging.StreamHandler()]
)


class RetrieveFirewallLogs:
    def __init__(self, root, fw_manager):
        self.entry_date = None
        logging.info("Initializing RetrieveFirewallLogs class")
        self.root = root
        self.fw_manager = fw_manager
        self.frame = tk.Frame(self.root, padx=270, pady=20)
        self.frame.pack(pady=50)
        logging.info("RetrieveFirewallLogs UI frame initialized")

    def open_window(self):
        logging.info("Opening RetrieveFirewallLogs window")

        label_date = tk.Label(self.frame, text="Retrieve logs older than (YYYY-MM-DD):")
        label_date.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_date = tk.Entry(self.frame, width=23)
        self.entry_date.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        logging.info("Date entry field created")

        get_logs_button = tk.Button(self.frame, text="Retrieve Logs", command=self.retrieve_logs)
        get_logs_button.grid(row=1, columnspan=2, pady=20)
        logging.info("Retrieve Logs button created")

        go_back_button = tk.Button(self.frame, text="Back to Homepage", command=self.back, width=20)
        go_back_button.grid(row=2, columnspan=2, pady=10)
        logging.info("Back to Homepage button created")

    def retrieve_logs(self):
        logging.info("Attempting to retrieve logs from firewall")
        date_str = self.entry_date.get()

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            logging.info(f"Formatted date for log retrieval: {formatted_date}")
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
            logging.error(f"Invalid date format: {ve}")
            return

        if self.fw_manager:
            config_commands = [f"execute log filter field time < {formatted_date}",
                               "execute log display"]
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

                    messagebox.showinfo("Success", f"Logs saved successfully at {file_path}.")
                    logging.info(f"Logs saved successfully at {file_path}")
                else:
                    messagebox.showwarning("Cancelled", "Save operation cancelled.")
                    logging.warning("Save operation cancelled by user.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve logs: {e}")
                logging.error(f"Failed to retrieve logs: {e}")
        else:
            messagebox.showerror("Error", "Firewall manager is not connected.")
            logging.error("Firewall manager is not connected.")

    def back(self):
        logging.info("Navigating back to homepage")
        self.frame.destroy()
        from .Homepage import HomePage
        home = HomePage(self.root, self.fw_manager)
        home.open_window()


if __name__ == "__main__":
    root_inst = tk.Tk()
    fw_manager_inst = FG_CLI_send_config.FirewallManager(host="192.168.10.99", username="admin", password="C@s@net")
    fw_manager_inst.connect()

    app = RetrieveFirewallLogs(root_inst, fw_manager_inst)
    app.open_window()
    root_inst.mainloop()
