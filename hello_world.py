from http import HTTPStatus

import streamlit as st
from aiven.client import AivenClient
from aiven.client.client import Error as AivenError

client = AivenClient(base_url="https://api.aiven.io")
st.write()


def authenticate(email : str, passwd : str, otp : str | None = None):
    result = client.authenticate_user(email=email, password=passwd, tenant_id="aiven", otp=otp)
    st.session_state.token = result["token"]
    st.session_state.email = email
    return result["token"]


@st.dialog("login")
def log_in():
    st.title("Log in")
    email = st.text_input("Email:")
    passwd = st.text_input("Password: ", type='password')
    otp = st.text_input("2 Factor Authentication OTP Code")
    if st.button("Log in"):
        token = authenticate(email=email, passwd=passwd, otp=otp)
        print("Authenticated without 2-factor auth")
        st.session_state.token = token
        st.session_state.email = email
        st.rerun()

@st.dialog("logout")
def log_out():
    st.title("Log out")
    st.write("Are you sure you want to log out?")
    if st.button("Yes"):
        st.session_state.email = None
        st.session_state.token = None
        st.rerun()
    if st.button("No"):
        st.rerun()


f"Session email: {st.session_state.get('email')}"
f"Session token: {st.session_state.get('token')}"

if st.session_state.get('email') is None:
    st.session_state
    log_in()
else:
    client.set_auth_token(st.session_state.get('token'))
    st.write(f"Logged in as {st.session_state.email}")
    if st.button("Log out"):
        log_out()

    st.write(client.get_user_info())
