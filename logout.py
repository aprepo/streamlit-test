import streamlit as st
import dialogs

client = st.session_state.get('client')
token_cache = st.session_state.get('token_cache')

#st.write(f"Logged in as {st.session_state.get('email')}")
user_info = client.get_user_info()
st.write(f"Logged in as {user_info.get('user')}")
if st.button("Log out"):
    dialogs.authentication.log_out(token_cache)
