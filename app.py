import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Sales', layout='wide')

start_date = dt.date.today() - dt.timedelta(days=30)
end_date   = dt.date.today()

# Sidebar  - global filters
with st.sidebar:
  st.header('Filters')
  region = st.selectbox('Region', ['All', 'N', 'S', 'E', 'W'])
  date_range = st.date_input('Date range', value=(start_date, end_date))

# Main area
st.title('Sales dashboard')

# KPI strip
df = load_and_filter(region, date_range)
c1, c2, c3 = st.columns(3)
c1.metric('Revenue', f'${df.sales.sum():,.0f}')
c2.metric('Orders', f'{len(df):,}')
c3.metric('AOV', f'${df.sales.mean():.2f}')

# Tabs for different views
tab1, tab2 = st.tabs(['Trends', 'Breakdown'])
with tab1:
  st.plotly_chart(make_trend_chart(df), use_container_width=True)
with tab2:
  st.plotly_chart(make_breakdown_chart(df), use_container_width=True)

with st.expander('Raw data'):
  st.dataframe(df)
