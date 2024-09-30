import streamlit as st
from aiven.client import AivenClient

client : AivenClient = st.session_state.get('client')

st.title("Projects")
user_info = client.get_user_info()
for project in user_info.get('projects'):
    st.write(project)

st.write(user_info)