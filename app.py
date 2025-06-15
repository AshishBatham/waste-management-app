import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

# Set Streamlit configuration
st.set_page_config(page_title="Waste Management Dashboard", layout="wide")

# App title and intro
st.title("♻️ Waste Management Optimization Dashboard")
st.markdown("""
This interactive dashboard visualizes waste generation data across countries, years, and materials to help identify reduction opportunities and forecast future trends.
""")

# Load data with caching
@st.cache_data
def load_data():
    return pd.read_csv("filtered_waste_data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters")
years = st.sidebar.multiselect("Select Year(s)", df['Year'].unique(), default=df['Year'].unique())
countries = st.sidebar.multiselect("Select Country(s)", df['Country'].unique(), default=df['Country'].unique())
materials = st.sidebar.multiselect("Select Material(s)", df['Material'].unique(), default=df['Material'].unique())

# Apply filters
filtered_df = df[
    (df['Year'].isin(years)) &
    (df['Country'].isin(countries)) &
    (df['Material'].isin(materials))
]

# CSV download
st.sidebar.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_waste_data.csv',
    mime='text/csv'
)

# Create tab layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Country-wise Waste", "📈 Forecasting", "🧱 Material-wise Waste", "🗃️ Raw Filtered Data"])

# --- Tab 1: Country-wise Waste ---
with tab1:
    st.subheader("📊 Top 10 Countries by Total Waste Generated")
    country_waste = filtered_df.groupby('Country')['Waste generated'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=country_waste.values, y=country_waste.index, palette="viridis", ax=ax)
    ax.set_xlabel("Total Waste Generated (Tons)")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# --- Tab 2: Forecasting ---
with tab2:
    st.subheader("📈 Forecast: Global Waste Generation")

    ts_df = df.groupby('Year')['Waste generated'].sum().reset_index()
    X = ts_df['Year'].values.reshape(-1, 1)
    y = ts_df['Waste generated'].values

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.array(range(ts_df['Year'].max()+1, ts_df['Year'].max()+6)).reshape(-1, 1)
    future_preds = model.predict(future_years)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ts_df['Year'], y, label="Historical", marker='o')
    ax.plot(future_years, future_preds, label="Forecast", linestyle='--', marker='x', color='red')
    ax.set_title("Forecast of Global Waste Generation")
    ax.set_xlabel("Year")
    ax.set_ylabel("Waste Generated (Tons)")
    ax.legend()
    st.pyplot(fig)

# --- Tab 3: Material-wise Waste ---
with tab3:
    st.subheader("🧱 Waste by Material Type")
    material_waste = filtered_df.groupby('Material')['Waste generated'].sum().sort_values()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=material_waste.values, y=material_waste.index, palette="mako", ax=ax)
    ax.set_xlabel("Total Waste Generated (Tons)")
    st.pyplot(fig)

# --- Tab 4: Raw Data ---
with tab4:
    st.subheader("🗃️ Filtered Data Preview")
    st.dataframe(filtered_df)
