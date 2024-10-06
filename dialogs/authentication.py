import streamlit as st
from aiven.client import AivenClient
from token_cache import TokenCache


def authenticate(client : AivenClient, email : str, passwd : str, otp : str | None = None):
    result = client.authenticate_user(email=email, password=passwd, tenant_id="aiven", otp=otp)
    st.session_state.token = result["token"]
    st.session_state.email = email
    return result["token"]


@st.dialog("login")
def log_in(client : AivenClient, token_cache: TokenCache):
    st.title("Log in")
    email = st.text_input("Email:")
    passwd = st.text_input("Password: ", type='password')
    otp = st.text_input("2 Factor Authentication OTP Code")
    if st.button("Log in"):
        token = authenticate(client=client, email=email, passwd=passwd, otp=otp)
        print("Authenticated without 2-factor auth")
        st.session_state.token = token
        token_cache.put_token(st.session_state.token)
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