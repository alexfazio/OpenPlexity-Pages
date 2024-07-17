import streamlit as st
import toggles_state

st.title('🎈 App Name')

st.write('Hello world!')

st.write("Debug: Before checkbox creation")

# Create the checkbox
checkbox_state = st.checkbox("My Checkbox", key="checkbox_state")

st.write("Debug: After checkbox creation")
st.write(f"Debug: checkbox_state value: {checkbox_state}")

# Update the external module's toggle state
toggles_state.update_toggle("checkbox_state", checkbox_state)

# Display the checkbox state
st.write(f"Checkbox state: {checkbox_state}")

# Display the toggle state from the external module
external_toggle_state = toggles_state.get_toggle("checkbox_state")
st.write(f"Toggle state in external module: {external_toggle_state}")

# Display all toggle states
all_toggles = toggles_state.get_all_toggles()
st.write("All toggle states:", all_toggles)

st.write("Debug: End of script")