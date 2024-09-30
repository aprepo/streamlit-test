from datetime import datetime
import streamlit as st
from aiven.client import AivenClient

client : AivenClient = st.session_state.get('client')

st.title("Billing groups")
billing_groups = client.get_billing_groups()

# Fetch the invoices for all the billing groups and create a dataframe
df = {
    'account_name': [],
    'billing_group_name': [],
    'billing_type' : [],
    'estimated_balance_usd' : [],
    'invoices' : []
}

for bg in billing_groups:
    for col in ['account_name', 'billing_group_name', 'billing_type', 'estimated_balance_usd']:
        df[col].append(bg.get(col))
    bg_id = bg.get('billing_group_id')
    total = []
    for invoice in client.list_billing_group_invoices(bg_id):
        timestamp = datetime.strptime(invoice.get('period_begin'), "%Y-%m-%dT%H:%M:%SZ")
        total.append(float(invoice.get('total_inc_vat', 0)))
    df['invoices'].append(total)


st.dataframe(df, column_config={
        'account_name': "Account",
        'billing_group_name': "Billing group",
        'billing_type' : "Type",
        'estimated_balance_usd' : "Balance (USD)",
        'invoices': st.column_config.BarChartColumn(
            "Historical spend"
        ),
})

st.write(df)
st.write(billing_groups)
