# toggles_helper.py

from toggle_states import toggle_states

def load_state():
    return toggle_states

def save_state(state):
    global toggle_states
    toggle_states = state

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

# Initialize default states if not already set
if not toggle_states:
    toggle_states = {
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