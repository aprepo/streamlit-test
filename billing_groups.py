from datetime import datetime
import streamlit as st
from aiven.client import AivenClient

client : AivenClient = st.session_state.get('client')


def load_billing_group_data():
    billing_groups = client.get_billing_groups()

    # Fetch the invoices for all the billing groups and create a dataframe
    df = {
        'account_name': [],
        'billing_group_name': [],
        'billing_type': [],
        'estimated_balance_usd': [],
        'total_spend': [],
        'invoices': [],
    }

    for bg in billing_groups:
        for col in ['account_name', 'billing_group_name', 'billing_type', 'estimated_balance_usd']:
            df[col].append(bg.get(col))
        bg_id = bg.get('billing_group_id')
        total = []
        total_spend = 0.0
        for invoice in client.list_billing_group_invoices(bg_id):
            timestamp = datetime.strptime(invoice.get('period_begin'), "%Y-%m-%dT%H:%M:%SZ")
            spend = float(invoice.get('total_inc_vat', 0))
            total.append(spend)
            total_spend += spend
        df['total_spend'].append(total_spend)
        df['invoices'].append(total)

    st.dataframe(df, column_config={
        'account_name': "Account",
        'billing_group_name': "Billing group",
        'billing_type': "Type",
        'estimated_balance_usd': st.column_config.NumberColumn(
            "Balance (in USD)",
            help="Current estimate invoice balance in USD",
            min_value=0,
            step=1,
            format="$%.2f",
        ),
        'total_spend': st.column_config.NumberColumn(
            "Total spend (in USD)",
            help="Total spend over time in USD",
            min_value=0,
            step=1,
            format="$%.2f",
        ),
        'invoices': st.column_config.BarChartColumn(
            "Historical spend"
        ),
    })
    return df, billing_groups

# Render the page. Show a spinner while the data is loading.
st.title("Billing groups")
with st.spinner(text="In progress..."):
    df, billing_groups = load_billing_group_data()
    st.write(df)
    st.write(billing_groups)

