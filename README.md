# FortiGate Firewall Management Tool

## Problem Statement

In today's digital landscape, managing network security is a critical task for any organization. Firewalls are the first line of defense against cyber threats, and configuring them correctly is paramount. However, managing firewall configurations, creating services, policies, and addresses can be cumbersome and prone to errors, especially when done manually via command-line interfaces. This project aims to simplify and streamline the management of FortiGate firewalls by providing a user-friendly graphical interface for performing common tasks.

## Solution Overview

This project provides a desktop application that offers an intuitive graphical user interface (GUI) to manage FortiGate firewalls. The application allows users to:

- **Create Firewall Addresses:** Add IP addresses to the firewall configuration with ease.
- **Create Firewall Services:** Define and manage network services (e.g., protocols and port ranges).
- **Create Firewall Policies:** Set up and manage firewall policies that control the traffic flow.
- **Retrieve and Export Data:** Fetch existing firewall addresses, services, and policies, and export them to CSV or text files.

By automating and simplifying these tasks, the tool reduces the likelihood of human error, improves efficiency, and makes firewall management accessible even to those with limited technical knowledge.

## Technologies Used

- **Python:** The core programming language used for developing the application.
- **Tkinter:** Python's standard library for creating graphical user interfaces (GUIs).
- **Netmiko:** A multi-vendor library that simplifies the management of network devices over SSH, used here for interacting with FortiGate firewalls.
- **FortiGate CLI:** Command-line interface commands specific to FortiGate devices are used for executing configurations and retrieving data.
- **CSV and Text Files:** For exporting firewall data, making it easy to store and review configurations.

## How the Problem is Solved

The application provides a set of predefined GUI forms where users can input necessary data (such as IP addresses, protocols, and port ranges) and execute firewall commands without having to manually type them out in a command-line environment. The process includes:

1. **Creating Firewall Addresses:** Users can specify IP addresses and names, which are then sent to the firewall as configuration commands.
2. **Creating Firewall Services:** Users can define services by specifying protocols, port ranges, and service names, which are then added to the firewall configuration.
3. **Managing Firewall Policies:** Users can create, select, and activate firewall policies directly from the GUI.
4. **Exporting Data:** The application allows users to retrieve all firewall addresses, services, and policies and save them to files in CSV or text format for documentation or further analysis.

This tool abstracts the complexity of command-line interactions, offering a more accessible and error-free approach to firewall management.

## How to Use

1. **Installation:**
   - Ensure Python is installed on your system.
   - Install required Python packages by running:
     ```bash
     pip install netmiko
     ```

2. **Launching the Application:**
   - Run the main script to start the application.
     ```bash
     python main.py
     ```
   - The GUI will open, offering various options like creating addresses, services, policies, and exporting firewall data.

3. **Configuration:**
   - Configure the firewall's connection details (IP address, username, password) in the `FirewallManager` class.

4. **Interacting with the Firewall:**
   - Use the GUI buttons to perform tasks such as adding addresses, services, and policies, or exporting data to files.

## Future Enhancements

- **User Authentication:** Add user authentication to restrict access to the application.
- **Enhanced Error Handling:** Improve error handling to provide more detailed feedback for troubleshooting.
- **Logging:** Implement logging to track user actions and firewall responses for auditing purposes.
- **Advanced Configuration:** Allow more complex configurations, such as NAT settings and VPN configurations, through the GUI.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
