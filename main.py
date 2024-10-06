import streamlit as st
from aiven.client import AivenClient
from token_cache import TokenCache
import dialogs
import settings


st.set_page_config(layout="wide")       # The page config needs to be the first call to st
client = AivenClient(base_url=settings.AIVEN_API_BASE_URL)
st.session_state.client = client


def main():
    token_cache = TokenCache(settings.SESSION_TOKEN_CACHE_FILENAME)
    if st.session_state.get('token') is None:
        # Try to first load the cached token and continue old auth session.
        # TODO: This should check if the token is expired or not
        # TODO: Logout should also clear the cache
        token = token_cache.get_token()
        if token is not None:
            print("Using cached token")
            st.session_state.token = token

    if st.session_state.get('token') is None:
        # If the user isn't logged in, and there was not cached session token,
        # just show the login dialog
        dialogs.authentication.log_in(client, token_cache)
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

if __name__ == "__main__":
    main()