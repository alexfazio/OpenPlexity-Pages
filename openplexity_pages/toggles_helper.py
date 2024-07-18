from toggle_states import toggle_states

# State Management Functions

def fetch_all_toggle_states():
    return toggle_states

def save_state(state):
    global toggle_states
    toggle_states = state

# Setter Functions

def update_global_toggle_state(key, value):
    state = fetch_all_toggle_states()
    state["global_tgl_elem"][key] = value
    save_state(state)

def update_block_toggle_state(block, key, value):
    state = fetch_all_toggle_states()
    if block not in state["blockwise_tgl_elem"]:
        state["blockwise_tgl_elem"][block] = {}
    state["blockwise_tgl_elem"][block][key] = value
    save_state(state)

# Getter Functions

def get_global_toggle_state(key, default=False):
    state = fetch_all_toggle_states()
    return state["global_tgl_elem"].get(key, default)

def get_block_toggle_state(block, key, default=False):
    state = fetch_all_toggle_states()
    return state["blockwise_tgl_elem"].get(block, {}).get(key, default)

# Initialization
if not toggle_states:
    toggle_states = {
        "global_tgl_elem": {
            "tgl_style": False,
            "tgl_target_audience": False,
            "tgl_persona": False,
            "tgl_exemplars": False,
        },
        "blockwise_tgl_elem": {
            "Zero": {"tgl_keywords": False},
            "One": {"tgl_keywords": False},
            "Two": {"tgl_keywords": False},
        }
    }