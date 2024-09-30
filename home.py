import streamlit as st

client = st.session_state.get('client')

st.title("Home")

user_info = client.get_user_info()
st.write(f"Welcome, {user_info.get('real_name')}")