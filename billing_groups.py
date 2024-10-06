from datetime import datetime
import streamlit as st
from aiven.client import AivenClient
import pandas as pd

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
        'invoices_with_timestamps': []
    }

    for bg in billing_groups:
        for col in ['account_name', 'billing_group_name', 'billing_type', 'estimated_balance_usd']:
            df[col].append(bg.get(col))
        bg_id = bg.get('billing_group_id')
        total = []
        total_spend = 0.0
        months = []
        for invoice in client.list_billing_group_invoices(bg_id):
            timestamp = datetime.strptime(invoice.get('period_begin'), "%Y-%m-%dT%H:%M:%SZ")
            spend = float(invoice.get('total_inc_vat', 0))
            total.append(spend)
            total_spend += spend
            months.append({'timestamp': timestamp, 'invoice': spend})
        df['total_spend'].append(total_spend)
        df['invoices'].append(total)
        df['invoices_with_timestamps'].append(months)
    return df, billing_groups

def refresh_billing_group_data_cache():
    st.session_state.billing_group_cache = load_billing_group_data()

def get_billing_group_data():
    if st.session_state.get('billing_group_cache') is None:
        refresh_billing_group_data_cache()
    return st.session_state.get('billing_group_cache')

def plot_spend_timeline(df_pivot):
    st.title("Spend timeline")
    st.write("The spend in each billing group in each month.")
    st.bar_chart(
        data=df_pivot,
        stack=True,
    )

def plot_invoice_summary_table(df_billing_groups):
    st.dataframe(
        df_billing_groups[
            [
                'account_name',
                'billing_group_name',
                'billing_type',
                'estimated_balance_usd',
                'total_spend',
                'invoices'
            ]
        ].sort_values(
            by='total_spend',
            ascending=False
        ),
        column_config={
            'account_name': "Organization",
            'billing_group_name': "Billing group",
            'billing_type': "Type",
            'estimated_balance_usd': st.column_config.ProgressColumn(
                "Balance (in USD)",
                help="Current estimate invoice balance in USD",
                min_value=0,
                max_value=df_billing_groups['estimated_balance_usd'].max(),
                format="$%.2f",
            ),
            'total_spend': st.column_config.ProgressColumn(
                "Total spend (in USD)",
                help="Total spend over time in USD",
                min_value=0,
                max_value=df_billing_groups['total_spend'].max(),
                format="$%.2f",
            ),
            'invoices': st.column_config.BarChartColumn(
                "Historical spend"
            )
        }
    )

def render_page():
    st.title("Billing groups")
    if st.button("Refresh"):
        with st.spinner(text="In progress..."):
            refresh_billing_group_data_cache()

    # Get the data for the page rendering
    df, billing_groups = get_billing_group_data()
    df_billing_groups = pd.DataFrame(data=df)

    # Flatten the 'invoices_with_timestamps' first, it is a list of dicts
    df_flattened = df_billing_groups[[
        'account_name',
        'invoices_with_timestamps'
    ]].explode('invoices_with_timestamps').reset_index(drop=True)

    # Then expand it so that we have the timestamp and invoice in separate
    # columns for the plotting of the graph
    df_expanded = pd.concat([
        df_flattened.drop('invoices_with_timestamps', axis=1),
        df_flattened['invoices_with_timestamps'].apply(pd.Series)
    ], axis=1)

    # Convert the timestamps to YYYY-MM format for better graph
    df_expanded['formatted_timestamp'] = pd.to_datetime(
        df_expanded['timestamp']
    ).dt.strftime('%Y-%m')

    # Draw the actual content to page
    plot_invoice_summary_table(df_billing_groups)
    plot_spend_timeline(
        df_expanded.pivot_table(
            index='formatted_timestamp',
            columns='account_name',
            values='invoice',
            aggfunc='sum'
        ).fillna(0)
    )

render_page()
