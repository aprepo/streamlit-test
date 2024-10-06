import pandas as pd
import streamlit as st
from aiven.client import AivenClient

client: AivenClient = st.session_state.get('client')

def refresh_org_cache():
    orgs = client.get_accounts()
    df = pd.DataFrame(orgs)
    df = df[[
        'account_id',
        'account_name',
        'organization_id',
        'tenant_id',
    ]]
    st.session_state.organizations = df
    return df

def get_org_dataframe():
    """
    Returns a cached org dataframe or fetches it from server if not found in
    cache.
    :return:
    """
    if st.session_state.get('organizations') is None:
        with st.spinner(text="Loading..."):
            return refresh_org_cache()
    else:
        return st.session_state.get('organizations')

def render_page():
    st.title("Home")

    user_info = client.get_user_info()
    st.write(f"Welcome, {user_info.get('real_name')}")

    st.title("Organizations")
    st.write("These are all the organizations you have access to.")

    if st.button("Refresh organizations"):
        with st.spinner(text="Loading..."):
            refresh_org_cache()

    df = get_org_dataframe()
    st.dataframe(df)


render_page()
