import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt



@st.cache_data
def load_data() -> pd.DataFrame:
    """Simulate a sales table — replace with your real query / CSV / DB call."""
    rng = np.random.default_rng(42)
    n = 500
    return pd.DataFrame({
        "order_date": pd.to_datetime(rng.integers(
            dt.date.today() - dt.timedelta(days=365),
            dt.date.today() + 1, n, dtype="datetime64")),
        "region":  rng.choice(["N", "S", "E", "W"], n),
        "product": rng.choice(["Widget", "Gadget", "Gizmo"], n),
        "sales":   rng.normal(100, 25, n).clip(5).round(2),
    })

def load_and_filter(region: str, date_range) -> pd.DataFrame:
    df = load_data()
    if date_range[0] is not None and date_range[1] is not None:
        d = df["order_date"].dt.normalize()
        df = df[(d >= pd.Timestamp(date_range[0])) & (d <= pd.Timestamp(date_range[1]))]
    if region != "All":
        df = df[df["region"] == region]
    return df

# ---------- chart builders (also stubs in the example) ----------

def make_trend_chart(df: pd.DataFrame) -> px.Figure:
    if df.empty:
        return px.line()  # empty placeholder figure
    daily = df.groupby(df["order_date"].dt.date)["sales"].sum().reset_index()
    daily = daily.rename(columns={"order_date": "date"})
    return px.line(daily, x="date", y="sales", labels={"sales": "Revenue ($)"})

def make_breakdown_chart(df: pd.DataFrame) -> px.Figure:
    if df.empty:
        return px.bar()
    agg = df.groupby("region")["sales"].sum().reset_index()
    return px.bar(agg, x="region", y="sales", color="region",
                  labels={"sales": "Revenue ($)", "region": "Region"})


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
