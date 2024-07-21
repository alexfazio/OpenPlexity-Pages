from toggle_states import toggle_states, toggle_states_structure

def reset_all_toggles():
    for key in toggle_states["global_tgl_elem"]:
        toggle_states["global_tgl_elem"][key] = False
    for block in toggle_states["block_level_tgl_elem"]:
        for key in toggle_states["block_level_tgl_elem"][block]:
            toggle_states["block_level_tgl_elem"][block][key] = False

def update_global_toggle_state(key, value):
    if key in toggle_states["global_tgl_elem"]:
        toggle_states["global_tgl_elem"][key] = value

def update_block_toggle_state(block, key, value):
    if block in toggle_states["block_level_tgl_elem"] and key in toggle_states["block_level_tgl_elem"][block]:
        toggle_states["block_level_tgl_elem"][block][key] = value

def get_global_toggle_state(key):
    return toggle_states["global_tgl_elem"].get(key, False)

def get_block_toggle_state(block, key):
    return toggle_states["block_level_tgl_elem"].get(block, {}).get(key, False)