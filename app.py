# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA

# Page settings
st.set_page_config(page_title="Waste Management Dashboard", layout="wide")
st.title("♻️ Waste Management Optimization Dashboard")
st.markdown("Analyze, forecast, and optimize waste management strategies using real-world data.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("waste_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region(s):", df['Region'].unique(), default=df['Region'].unique())
df_filtered = df[df['Region'].isin(selected_region)]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Trends", "🔀 Clustering", "📈 Forecasting", "🏭 Facility Analysis"])

# 1. EDA
with tab1:
    st.subheader("Waste Generation Over Time")
    waste_over_time = df_filtered.groupby('Date')['Total_Waste'].sum()
    st.line_chart(waste_over_time)

    st.subheader("Recycled Waste by Region")
    region_recycle = df_filtered.groupby('Region')['Recycled_Waste'].mean().sort_values(ascending=False)
    st.bar_chart(region_recycle)

# 2. Clustering
with tab2:
    st.subheader("Waste Composition Clustering")
    waste_cols = ['Organic', 'Plastic', 'Metal', 'Glass']
    X = df_filtered[waste_cols]

    kmeans = KMeans(n_clusters=3, random_state=42)
    df_filtered['Cluster'] = kmeans.fit_predict(X)

    fig, ax = plt.subplots()
    sns.scatterplot(data=df_filtered, x='Organic', y='Plastic', hue='Cluster', palette='tab10', ax=ax)
    st.pyplot(fig)

# 3. Forecasting
with tab3:
    st.subheader("Waste Generation Forecast (ARIMA)")
    df_ts = df_filtered.groupby('Date')['Total_Waste'].sum()

    try:
        model = ARIMA(df_ts, order=(1,1,1))
        result = model.fit()
        forecast = result.forecast(steps=12)

        fig, ax = plt.subplots()
        df_ts.plot(label='Actual', ax=ax)
        forecast.plot(label='Forecast', ax=ax, color='orange')
        plt.legend()
        plt.title("12-Month Forecast")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"ARIMA model error: {e}")

# 4. Facility Performance
with tab4:
    st.subheader("Facility Performance Overview")
    if 'Facility' in df.columns:
        facility_metrics = df_filtered.groupby('Facility')[['Efficiency', 'Recycled_Waste']].mean()
        st.dataframe(facility_metrics.style.highlight_max(axis=0))

        fig, ax = plt.subplots()
        facility_metrics.plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
        plt.title("Facility Metrics")
        st.pyplot(fig)
    else:
        st.warning("Facility data not available in dataset.")

