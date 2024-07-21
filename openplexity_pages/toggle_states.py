# Define the structure
toggle_states_structure = {
    "global_tgl_elem": [
        "tgl_style",
        "tgl_target_audience",
        "tgl_persona",
        "tgl_exemplars"
    ],
    "block_level_tgl_elem": [
        "Zero",
        "One",
        "Two",
        "Introduction",
        "Main",
        "Conclusion"
    ],
    "block_level_toggles": [
        "tgl_keywords",
        "tgl_notes"
    ]
}

# Initialize the actual toggle states
toggle_states = {
    "global_tgl_elem": {toggle: False for toggle in toggle_states_structure["global_tgl_elem"]},
    "block_level_tgl_elem": {
        block: {toggle: False for toggle in toggle_states_structure["block_level_toggles"]}
        for block in toggle_states_structure["block_level_tgl_elem"]
    }
}