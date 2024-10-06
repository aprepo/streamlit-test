import pandas as pd
import streamlit as st
from aiven.client import AivenClient

client: AivenClient = st.session_state.get('client')

# Monkeypatching the client that is missing the feature I need to get the
# organization events. This should be really contributed to the client code.
def get_org_events(self, account_id):
    return self.verify(
        self.get,
        self.build_path("account", account_id, "events"),
        params={'limit':100},
        result_key="events"
    )
AivenClient.get_org_events = get_org_events

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
    if st.session_state.get('organizations') is None:
        with st.spinner(text="Loading..."):
            return refresh_org_cache()
    else:
        return st.session_state.get('organizations')

def refresh_events(df_accounts, df):
    all_events = pd.DataFrame([])
    for account_id in df_accounts:
        events = client.get_org_events(account_id)
        if events:
            events_df = pd.DataFrame(events).merge(
                df[['account_id', 'account_name']],
                on='account_id',
                how='left'
            )[[
                'account_id',
                'account_name',
                'create_time',
                'action_description',
                'actor',
                'actor_user_id'
            ]]
            all_events = pd.concat([all_events, events_df], ignore_index=True)
    all_events = all_events.sort_values(
        by='create_time',
        ascending=False
    )
    st.session_state.org_events = all_events
    return all_events

def get_org_events(df_accounts, df):
    if st.session_state.get('org_events') is None:
        return refresh_events(df_accounts, df)
    else:
        return st.session_state.get('org_events')

def show_org_event_stream(df_accounts, df):
    st.title("Organization events")
    if st.button("Refresh events"):
        refresh_events(df_accounts, df)
    all_events = get_org_events(df_accounts, df)
    st.dataframe(all_events)

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

    df_accounts = df['account_id'].unique()
    show_org_event_stream(df_accounts, df)


render_page()
