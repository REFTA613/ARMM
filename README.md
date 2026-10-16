
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

    git clone https://github.com/REFTA613/ARMM.git
    cd ARMM

Create the virtual environment and install the Python dependencies:

    bash setup.sh

The setup script creates a local virtual environment named `venv` and installs the dependencies listed in `requirements.txt`.

The current dependency list includes `requests`.

## Usage

### Use the Default Configuration Path

Run:

    bash run.sh

By default, ARMM looks for the following configuration file:

    /home/armareforger1/serverfiles/armarserver_config.json

This default path is specific to the current implementation. If your LinuxGSM installation uses a different account or directory, provide the correct path explicitly.

### Specify a Custom Configuration File

Pass the absolute path to the JSON configuration file:

    bash run.sh /absolute/path/to/armarserver_config.json

For paths containing spaces, use quotes:

    bash run.sh "/path/to/my server/armarserver_config.json"

### Review Proposed Changes

When outdated versions are detected, ARMM displays the configured and retrieved versions and asks for confirmation:

    Update config file with new versions? (yes/no):

Enter `yes` to proceed. Any other response aborts the update.

Review the proposed changes carefully before confirming.

## Backups and Recovery

Before writing changes, ARMM creates a backup alongside the configuration file.

For example:

    armarserver_config.json
    armarserver_config.json.backup

If an error occurs while writing the updated configuration, the program attempts to restore the backup automatically.

For manual recovery, stop any process that might modify the same configuration file, then restore the backup using your preferred file-management procedure.

**Backup warning:** the current implementation uses a fixed `.backup` filename. A subsequent update can overwrite an existing backup. Preserve any backup you need to keep before running another update.

## Version Checks and Limitations

- Workshop lookups depend on the availability and structure of the public Workshop pages.
- A failed lookup does not necessarily mean that a mod has been deleted; it may be temporarily unavailable or inaccessible.
- Version comparison extracts numeric components and compares up to three components. It is not a complete implementation of semantic versioning.
- The tool updates configuration version values; it does not download, install, or validate mod content.
- The current implementation supports specific JSON mod-list structures. Other configuration formats may require code changes.
- Configuration updates should be followed by appropriate server checks before returning the server to normal operation.

## Troubleshooting

### The Configuration File Cannot Be Opened

Verify the path and ensure the user running ARMM has permission to read the file.

### Python Dependencies Are Missing

Run the setup script again:

    bash setup.sh

Ensure Python 3 and its virtual-environment support are installed.

### A Mod Cannot Be Resolved

Check the mod ID and its availability on the official Workshop. Retry later if the service is temporarily unavailable.

### The Configuration Does Not Contain a Recognized Mod List

Verify that the JSON file contains a supported mod-list structure and that it is valid JSON.

## Project Structure

    ARMM/
    ├── armm.py
    ├── requirements.txt
    ├── run.sh
    ├── setup.sh
    ├── README.md
    └── LICENSE

## License

ARMM is distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Fabio Clemente — [REFTA613](https://github.com/REFTA613)
