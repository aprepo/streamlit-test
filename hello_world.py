import streamlit as st
from aiven.client import AivenClient
import dialogs

client = AivenClient(base_url="https://api.aiven.io")

f"Session email: {st.session_state.get('email')}"
f"Session token: {st.session_state.get('token')}"

if st.session_state.get('email') is None:
    dialogs.authentication.log_in(client)
else:
    client.set_auth_token(st.session_state.get('token'))
    st.write(f"Logged in as {st.session_state.email}")
    if st.button("Log out"):
        dialogs.authentication.log_out()

    st.write(client.get_user_info())
