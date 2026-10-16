# ARMM — Arma Reforger Mod Version Manager

ARMM is a Python command-line utility for checking Arma Reforger Workshop mod versions against the versions recorded in a LinuxGSM server configuration.

It helps server administrators identify outdated mod version entries and update the configuration after reviewing the proposed changes.

## Features

- **Workshop version checks:** queries the public Arma Reforger Workshop for the current version of each configured mod.
- **Version comparison:** compares configured versions with the versions retrieved from the Workshop.
- **Interactive updates:** displays proposed changes and asks for confirmation before modifying the configuration.
- **Automatic backup:** creates a backup of the configuration before writing changes.
- **Custom configuration path:** accepts an alternative JSON configuration file as a command-line argument.
- **Request handling:** uses HTTP timeouts, limited retries and delays between Workshop requests.
- **Error reporting:** reports mods that cannot be found or whose versions cannot be retrieved.

## How It Works

1. ARMM reads the server configuration JSON file.
2. It identifies the configured mod IDs and their recorded versions.
3. It queries the Arma Reforger Workshop for the current version of each mod.
4. It reports version differences and mods whose versions could not be retrieved.
5. If updates are available, it asks for confirmation.
6. After confirmation, it creates a backup and updates the corresponding version values in the configuration file.

**Important:** ARMM updates version entries in the configuration file. It does not download or install mod files, remove outdated mod files, restart the server, or verify that updated mods work correctly in-game.

## Requirements

- Linux environment.
- Python 3 with the `venv` module available.
- Network access to the public Arma Reforger Workshop.
- A valid JSON configuration file containing the server's mod entries.
- Read and write permissions for the configuration file and its directory.

The server configuration is expected to use a supported mod-list structure, such as `game.mods` or a root-level `mods` array.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/REFTA613/ARMM.git
cd ARMM