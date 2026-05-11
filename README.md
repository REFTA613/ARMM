![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-LinuxGSM-lightgrey.svg)

# Arma Reforger Mod Version Checker & Updater for LinuxGSM


A command-line utility designed specifically for LinuxGSM-managed Arma Reforger server instances.  
This tool automates the process of checking workshop mod versions, comparing them against the latest releases, and safely updating the server configuration file.

---

## Features

- Automated version comparison against the official Arma Reforger Workshop  
- Safe configuration updates with automatic backup creation  
- Native support for LinuxGSM directory structure and `game.mods` configuration format  
- Built-in rate limiting and HTTP session management to prevent API throttling  
- Command-line argument support for custom configuration paths  
- Graceful handling of unpublished, removed, or temporarily unavailable mods  

---

## Prerequisites

- Linux environment running an Arma Reforger server via LinuxGSM  
- Python 3.6 or higher  
- Python `requests` library  
- Active network connectivity to `reforger.armaplatform.com`  

---

## Installation

1. Navigate to your main user directory.

2. Clone the repository into the main directory.
```
git clone https://github.com/your-username/reforger-mod-updater.git
```
3. Set executable permissions for the project directory.
```
chmod 755 ARMM
```
4. Enter the project directory.
```
cd ARMM
```
5. Run the setup script to initialize dependencies.
```
./setup.py
```
---

## Usage

Execute the main script:
```
./setup.py
```

The tool will automatically:

- Load the default configuration file from  
  `/home/armareforger1/serverfiles/armarserver_config.json`
- Parse the `game.mods` array from the configuration
- Query the official workshop for each installed mod ID
- Compare local versions against remote versions
- Display a summary of outdated or unreachable mods
- Prompt for confirmation before modifying the configuration
- Generate a `.backup` file and apply updates upon approval

---

### Custom configuration file

To use a custom configuration file, pass the absolute path as an argument:


---

## Technical Notes

- The utility queries public workshop pages directly. No private API credentials are required.  
- Mods marked as unreachable are typically unpublished, removed, or temporarily offline on the workshop.  
- Version comparison follows standard semantic versioning logic. Non-standard version strings are handled without interrupting execution.  
- Network requests include controlled delays to comply with workshop rate limits and prevent connection throttling.  
- A configuration backup is generated in the same directory before any modifications are written. Retain backup files for manual rollback if required.  
- Always verify server stability after applying mod version updates.  

---


## Author
Fabio Clemente (REFTA)

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
