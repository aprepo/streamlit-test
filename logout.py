import streamlit as st
import dialogs

st.write(f"Logged in as {st.session_state.email}")
if st.button("Log out"):
    dialogs.authentication.log_out()
