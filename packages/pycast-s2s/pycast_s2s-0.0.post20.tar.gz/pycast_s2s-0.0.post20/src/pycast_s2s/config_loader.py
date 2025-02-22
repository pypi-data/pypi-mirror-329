import json
import os
from pathlib import Path

# Get the absolute path of the conf/ directory
CONF_DIR = Path(__file__).parent / "conf"

def load_json(filename):
    """Load a JSON config file from the conf directory."""
    file_path = CONF_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file {filename} not found in {CONF_DIR}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Example usage
if __name__ == "__main__":
    domain_config = load_json("domain_config.json")
    print(domain_config)