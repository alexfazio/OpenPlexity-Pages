import streamlit as st
from toggles_state import toggle_states

st.title('🎈 App Name')

st.write('Hello world!')

st.write("Debug: Before checkbox creation")

# Create the checkbox
checkbox_state = st.checkbox("My Checkbox", key="checkbox_state")

st.write("Debug: After checkbox creation")
st.write(f"Debug: checkbox_state value: {checkbox_state}")

# Update the external module's toggle state
toggle_states["checkbox_state"] = checkbox_state

# Display the checkbox state
st.write(f"Checkbox state: {checkbox_state}")

# Display the toggle state from the external module
external_toggle_state = toggle_states.get("checkbox_state", False)
st.write(f"Toggle state in external module: {external_toggle_state}")

# Display all toggle states
st.write("All toggle states:", toggle_states)

st.write("Debug: End of script")