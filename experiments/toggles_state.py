# toggles_state.py

# Dictionary to store toggle states
toggle_states = {}

def update_toggle(key, value):
    """Update the state of a toggle."""
    toggle_states[key] = value

def get_toggle(key):
    """Get the state of a toggle."""
    return toggle_states.get(key, False)  # Default to False if key doesn't exist

def get_all_toggles():
    """Get all toggle states."""
    return toggle_states