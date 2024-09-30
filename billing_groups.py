import streamlit as st
from aiven.client import AivenClient

client : AivenClient = st.session_state.get('client')

st.title("Billing groups")
billing_groups = client.get_billing_groups()
df = {
    'account_name': [],
    'billing_group_name': [],
    'billing_type' : [],
    'estimated_balance_usd' : []
}

for bg in billing_groups:
    for col in ['account_name', 'billing_group_name', 'billing_type', 'estimated_balance_usd']:
        df[col].append(bg.get(col))

st.dataframe(df, column_config={
        'account_name': "Account",
        'billing_group_name': "Billing group",
        'billing_type' : "Type",
        'estimated_balance_usd' : "Balance (USD)"
})

st.write(billing_groups)
