import json
import re
import time
import requests
import sys
import shutil

REQUEST_DELAY = 0.5
MAX_RETRIES = 2

# =====================
# COLORS
# =====================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def ok(x): print(f"{GREEN}[OK]{RESET} {x}")
def info(x): print(f"{BLUE}[INFO]{RESET} {x}")
def warn(x): print(f"{YELLOW}[WARN]{RESET} {x}")
def err(x): print(f"{RED}[ERROR]{RESET} {x}")


# =====================
# LOAD CONFIG
# =====================

def load_config(path):
    info(f"Loading config: {path}")
    with open(path, "r") as f:
        return json.load(f)


# =====================
# FIND MODS
# =====================

def get_mods(config):
    mods = None

    if "mods" in config and isinstance(config["mods"], list):
        mods = config["mods"]
        info("Found mods at root level: 'mods'")
    elif "game" in config and isinstance(config["game"], dict):
        if "mods" in config["game"] and isinstance(config["game"]["mods"], list):
            mods = config["game"]["mods"]
            info("Found mods nested in: 'game.mods'")

    if not mods:
        for key in ["workshop_mods", "installed_mods", "modList", "server_mods"]:
            if key in config and isinstance(config[key], list):
                mods = config[key]
                info(f"Found mods under alternative key: '{key}'")
                break

    if not mods or not isinstance(mods, list):
        err("Unable to find a mod list in the config")
        err(f"Available root keys: {list(config.keys())}")
        if "game" in config:
            err(f"Keys in 'game': {list(config['game'].keys())}")
        return []

    ok(f"Found {len(mods)} mods in config")

    parsed = []
    for m in mods:
        if isinstance(m, dict):
            mod_id = m.get("modId") or m.get("id") or m.get("mod_id")
            version = m.get("version") or m.get("currentVersion") or m.get("currentVersionNumber", "0.0.0")
            if mod_id:
                parsed.append({
                    "modId": str(mod_id).strip(),
                    "version": str(version).strip()
                })

    return parsed


# =====================
# REMOTE VERSION LOOKUP
# =====================

def get_remote_version(session, mod_id):
    url = f"https://reforger.armaplatform.com/workshop/{mod_id}"
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = session.get(url, timeout=15)
            r.raise_for_status()
            
            match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text, re.DOTALL)
            if not match:
                if attempt < MAX_RETRIES:
                    time.sleep(1)
                    continue
                return None
                
            data = json.loads(match.group(1))
            asset = data.get("props", {}).get("pageProps", {}).get("asset")
            
            if asset and "currentVersionNumber" in asset:
                return str(asset["currentVersionNumber"])
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            return None
        except (json.JSONDecodeError, KeyError, requests.RequestException):
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            return None
            
    return None


# =====================
# VERSION CHECK
# =====================

def version(v, parts=3):
    nums = re.findall(r"\d+", str(v))
    nums = [int(n) for n in nums[:parts]]
    while len(nums) < parts:
        nums.append(0)
    return tuple(nums)

def outdated(local, remote):
    return version(local) < version(remote)


# =====================
# MAIN
# =====================

def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "/home/armareforger1/serverfiles/armarserver_config.json"
    info(f"Using config: {config_path}")

    config = load_config(config_path)
    ok("Config loaded")

    mods = get_mods(config)
    if not mods:
        return

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html"
    })

    updates = []
    not_found = []
    total = len(mods)

    info(f"Starting version check for {total} mods (est. {total * REQUEST_DELAY:.0f}s)...")

    for i, mod in enumerate(mods):
        mod_id = mod["modId"]
        local_v = mod["version"]

        info(f"[{i+1}/{total}] Checking {mod_id}")

        remote_v = get_remote_version(session, mod_id)
        time.sleep(REQUEST_DELAY)

        if remote_v is None:
            warn(f"NOT FOUND OR UNREACHABLE: {mod_id}")
            not_found.append(mod_id)
            continue

        info(f"Local: {local_v} -> Remote: {remote_v}")

        if outdated(local_v, remote_v):
            warn(f"UPDATE REQUIRED: {mod_id}")
            updates.append({"id": mod_id, "local": local_v, "remote": remote_v})

    if not updates:
        ok("All reachable mods are up to date.")
        if not_found:
            warn(f"{len(not_found)} mods were not found on the workshop.")
        return

    print(f"\n{len(updates)} mods require update:")
    for u in updates:
        print(f"  {u['id']} : {u['local']} -> {u['remote']}")

    if not_found:
        print(f"\n{len(not_found)} mods could not be resolved:")
        for nf in not_found:
            print(f"  - {nf}")

    choice = input("Update config file with new versions? (yes/no): ").strip().lower()
    if choice != "yes":
        warn("Aborted.")
        return

    # Create backup
    backup_path = f"{config_path}.backup"
    try:
        shutil.copy2(config_path, backup_path)
        info(f"Backup created: {backup_path}")
    except Exception as e:
        err(f"Failed to create backup: {e}")
        return

    # Map updates
    update_map = {u["id"]: u["remote"] for u in updates}
    updated_count = 0

    # Locate mod list in config structure
    target_mods = []
    if "game" in config and isinstance(config["game"], dict):
        target_mods = config["game"].get("mods", [])
    if not target_mods and "mods" in config:
        target_mods = config["mods"]

    # Apply version updates
    for mod in target_mods:
        mod_id = mod.get("modId") or mod.get("id")
        if mod_id and mod_id in update_map:
            mod["version"] = update_map[mod_id]
            updated_count += 1

    # Write updated config
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        ok(f"Config file updated successfully. {updated_count} versions modified.")
    except Exception as e:
        err(f"Error writing file: {e}")
        warn("Restoring backup...")
        try:
            shutil.copy2(backup_path, config_path)
            ok("Backup restored.")
        except Exception as e2:
            err(f"Failed to restore backup: {e2}")


if __name__ == "__main__":
    main()