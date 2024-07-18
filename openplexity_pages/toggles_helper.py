# toggles_helper.py

import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "toggle_states.json"

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "global": {},
        "blocks": {}
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def update_global_toggle_state(key, value):
    state = load_state()
    state["global"][key] = value
    save_state(state)

def update_block_toggle_state(block, key, value):
    state = load_state()
    if block not in state["blocks"]:
        state["blocks"][block] = {}
    state["blocks"][block][key] = value
    save_state(state)

def get_global_toggle_state(key, default=False):
    state = load_state()
    return state["global"].get(key, default)

def get_block_toggle_state(block, key, default=False):
    state = load_state()
    return state["blocks"].get(block, {}).get(key, default)

# Initialize default states if the file doesn't exist
if not STATE_FILE.exists():
    default_state = {
        "global": {
            "tgl_style": False,
            "tgl_target_audience": False,
            "tgl_persona": False,
            "tgl_exemplars": False,
        },
        "blocks": {
            "Zero": {"tgl_keywords": False},
            "One": {"tgl_keywords": False},
            "Two": {"tgl_keywords": False},
        }
    }
    save_state(default_state)