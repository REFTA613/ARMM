![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-LinuxGSM-lightgrey.svg)

### ARMM – Arma Reforger Mod Manager for LinuxGSM

ARMM is a plugin for LinuxGSM that automates the management and updating of mods for Arma Reforger dedicated servers.

It is designed to remove the manual process of downloading, updating, and syncing mods, making server maintenance faster, safer, and less error-prone.

## What problem does it solve?

Managing mods for Arma Reforger servers manually is often:

slow and repetitive

error-prone (missing files, wrong versions)

hard to keep synchronized across servers

ARMM solves this by automating the entire mod update workflow inside LinuxGSM.

## What it does

ARMM integrates into LinuxGSM and provides tools to:

Download and update Arma Reforger mods

Synchronize mod versions with server configuration

Clean outdated or unused mod files

Ensure consistency between server and mod repository

Key idea

Instead of manually handling mod files, ARMM acts as an automation layer on top of LinuxGSM.

“One command to keep your server mods up to date.”

## Tech / Environment

LinuxGSM compatible environment

Bash / scripting integration (or plugin system depending on implementation)

Designed for dedicated Arma Reforger servers

## Why this project exists

This tool was built to simplify real server administration workflows, especially for communities hosting Arma Reforger servers that rely on frequent mod updates.

Future improvements

Web dashboard for mod management

Auto-detection of mod updates

Multi-server synchronization support

(Optional)

Add screenshots or terminal output here showing:

mod update process

LinuxGSM integration

before/after sync state






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
git clone https://github.com/$user/ARMM.git
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
./run.py
```

The tool will automatically:

- Load the default configuration file from  
  `$user/serverfiles/armarserver_config.json`
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
Fabio Clemente (REFTA613)

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
