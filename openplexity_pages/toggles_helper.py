from toggle_states import toggle_states_structure

# Initialize the toggle states with all values set to False
def initialize_toggle_states():
    toggle_states = {
        "global_tgl_elem": {toggle: False for toggle in toggle_states_structure["global_tgl_elem"]},
        "blockwise_tgl_elem": {
            block: {toggle: False for toggle in toggle_states_structure["blockwise_toggles"]}
            for block in toggle_states_structure["blockwise_tgl_elem"]
        }
    }
    return toggle_states

# Use a global variable to store the current state
current_toggle_states = initialize_toggle_states()

# State Management Functions

def fetch_all_toggle_states():
    return current_toggle_states

def save_state(state):
    global current_toggle_states
    current_toggle_states = state

# Setter Functions

def update_global_toggle_state(key, value):
    state = fetch_all_toggle_states()
    if key in state["global_tgl_elem"]:
        state["global_tgl_elem"][key] = value
        save_state(state)

def update_block_toggle_state(block, key, value):
    state = fetch_all_toggle_states()
    if block in state["blockwise_tgl_elem"] and key in state["blockwise_tgl_elem"][block]:
        state["blockwise_tgl_elem"][block][key] = value
        save_state(state)

# Getter Functions

def get_global_toggle_state(key):
    state = fetch_all_toggle_states()
    return state["global_tgl_elem"].get(key, False)

def get_block_toggle_state(block, key):
    state = fetch_all_toggle_states()
    return state["blockwise_tgl_elem"].get(block, {}).get(key, False)

# Add this function to reset all toggles to False
def reset_all_toggles():
    global current_toggle_states
    current_toggle_states = initialize_toggle_states()

# Initialize the toggle states
current_toggle_states = initialize_toggle_states()