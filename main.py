import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
if "data_generated" not in st.session_state:
    st.session_state.data_generated = False
if "user_theme" not in st.session_state:
    st.session_state.user_theme = "Blue"

# ==========================================
# 3. HELPER FUNCTIONS & CACHING
# ==========================================
@st.cache_data
def load_sample_data(num_rows: int = 500) -> pd.DataFrame:
    """Generates synthetic sales data cached for performance."""
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=num_rows, freq="D")
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Clothing", "Home & Garden", "Books"]
    
    df = pd.DataFrame({
        "Date": dates,
        "Region": np.random.choice(regions, num_rows),
        "Category": np.random.choice(categories, num_rows),
        "Sales": np.random.uniform(50, 1000, num_rows).round(2),
        "Units_Sold": np.random.randint(1, 20, num_rows),
        "Satisfaction": np.random.uniform(3.0, 5.0, num_rows).round(1)
    })
    return df

# Initialize Data
df = load_sample_data()

# ==========================================
# 4. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    st.title("Settings & Filters")
    
    st.subheader("Data Filters")
    selected_regions = st.multiselect(
        "Select Regions",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )
    
    selected_categories = st.multiselect(
        "Select Categories",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )
    
    min_sales, max_sales = st.slider(
        "Sales Range ($)",
        min_value=float(df["Sales"].min()),
        max_value=float(df["Sales"].max()),
        value=(float(df["Sales"].min()), float(df["Sales"].max()))
    )
    
    st.divider()
    
    st.subheader("App Controls")
    enable_animations = st.checkbox("Simulate Live Data Refresh", value=False)
    
    if st.button("Clear Cache", type="secondary"):
        st.cache_data.clear()
        st.toast("Cache cleared successfully!", icon="🧹")

# Filter DataFrame based on inputs
filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Sales"].between(min_sales, max_sales))
]

# ==========================================
# 5. MAIN CONTENT AREA
# ==========================================
st.title("📊 Enterprise Analytics Portal")
st.caption("Interactive data exploration platform built with Streamlit")

if enable_animations:
    with st.spinner("Fetching latest updates..."):
        time.sleep(0.8)

# Metric Summary Cards
col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df["Sales"].sum()
total_units = filtered_df["Units_Sold"].sum()
avg_satisfaction = filtered_df["Satisfaction"].mean() if not filtered_df.empty else 0
record_count = len(filtered_df)

col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}", delta="12.5%")
col2.metric(label="Units Sold", value=f"{total_units:,}", delta="-2.1%")
col3.metric(label="Avg Satisfaction", value=f"{avg_satisfaction:.2f} / 5.0", delta="0.4")
col4.metric(label="Active Records", value=f"{record_count:,}")

st.divider()

# Tabbed Layout
tab_charts, tab_data, tab_upload = st.tabs(["📈 Visualizations", "📋 Data Explorer", "📤 Upload Custom Data"])

# TAB 1: Visualizations
with tab_charts:
    st.subheader("Performance Breakdown")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Sales Trend Over Time**")
        if not filtered_df.empty:
            daily_sales = filtered_df.groupby("Date")["Sales"].sum().reset_index()
            fig_line = px.line(daily_sales, x="Date", y="Sales", template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No data available for selected filters.")
            
    with chart_col2:
        st.markdown("**Revenue by Region & Category**")
        if not filtered_df.empty:
            fig_bar = px.bar(
                filtered_df, 
                x="Region", 
                y="Sales", 
                color="Category", 
                barmode="group",
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

# TAB 2: Data Explorer
with tab_data:
    st.subheader("Filtered Dataset")
    st.markdown("Double-click cells to inspect raw data or use search bar.")
    
    # Interactive Dataframe
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Sales": st.column_config.NumberColumn("Revenue ($)", format="$%.2f"),
            "Satisfaction": st.column_config.ProgressColumn(
                "Customer Rating", min_value=1, max_value=5, format="%.1f"
            ),
            "Date": st.column_config.DateColumn("Transaction Date")
        },
        hide_index=True
    )
    
    # Download Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv_data,
        file_name="analytics_export.csv",
        mime="text/csv",
    )

# TAB 3: File Upload & Custom Analysis
with tab_upload:
    st.subheader("Upload Custom CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        custom_df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        
        with st.expander("Preview Uploaded Data", expanded=True):
            st.dataframe(custom_df.head(10), use_container_width=True)
            st.write(f"**Shape:** {custom_df.shape[0]} rows, {custom_df.shape[1]} columns")
    else:
        st.info("Upload a custom dataset above to explore its raw structure.")
