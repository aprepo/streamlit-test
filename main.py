import streamlit as st
from aiven.client import AivenClient
import dialogs

client = AivenClient(base_url="https://api.aiven.io")
st.set_page_config(layout="wide")
st.session_state.client = client

if st.session_state.get('token') is None:
    # If the user isn't logged in, just show the
    # login dialog
    dialogs.authentication.log_in(client)
else:
    # User is logged in. Store the auth token to the client.
    client.set_auth_token(st.session_state.get('token'))

    # Create the pages and register them to the navigation
    page_home = st.Page("home.py", title="Home")
    page_projects = st.Page("projects.py", title="Projects")
    page_billing_groups = st.Page("billing_groups.py", title="Billing groups")
    page_logout = st.Page("logout.py", title="Logout")
    pg = st.navigation([
        page_home,
        page_projects,
        page_billing_groups,
        page_logout,
    ])
    pg.run()
