import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#PAGE CONFIG
st.set_page_config(
    page_title="Data Insight Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  ENHANCED CSS 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern gradient background */
    body, .main, .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 25%, #ffe4e6 50%, #fce7f3 75%, #fef3f2 100%) !important;
        animation: gradient-shift 15s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px !important;
    }
    
    /* Main page title only */
    .main > div > div > div > h1:first-of-type {
        font-size: 3.2rem !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #dc2626 0%, #e11d48 50%, #be123c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Regular h1 */
    h1 {
        font-size: 3.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        margin-bottom: 1.2rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
        color: #0f172a !important;
    }
    
    .subtitle {
        color: #475569 !important;
        font-size: 18px !important;
        margin-bottom: 40px !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
    }
    
    p {
        color: #334155 !important;
        line-height: 1.6 !important;
    }
    
    /* Premium card styling with glassmorphism */
    .card {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        padding: 40px !important;
        border-radius: 24px !important;
        border: 1px solid rgba(220, 38, 38, 0.1) !important;
        box-shadow: 
            0 20px 60px rgba(220, 38, 38, 0.08),
            0 0 0 1px rgba(255, 255, 255, 0.8) inset !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 28px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(220, 38, 38, 0.05), transparent);
        transition: left 0.5s;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-6px) scale(1.01) !important;
        box-shadow: 
            0 30px 80px rgba(220, 38, 38, 0.15),
            0 0 0 1px rgba(255, 255, 255, 1) inset !important;
        border-color: rgba(220, 38, 38, 0.2) !important;
    }
    
    /* Stunning metric cards */
    .metric {
        background: linear-gradient(135deg, #dc2626 0%, #e11d48 50%, #be123c 100%) !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 48px 32px !important;
        text-align: center !important;
        box-shadow: 
            0 20px 60px rgba(220, 38, 38, 0.35),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    
    .metric:hover {
        transform: translateY(-8px) scale(1.03) !important;
        box-shadow: 
            0 30px 80px rgba(220, 38, 38, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
    }
    
    .metric h1 {
        color: #ffffff !important;
        font-size: 56px !important;
        margin: 0 !important;
        font-weight: 900 !important;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
        letter-spacing: -2px !important;
        position: relative !important;
        z-index: 1 !important;
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: #ffffff !important;
        background-clip: unset !important;
    }
    
    .metric p {
        color: #fecaca !important;
        font-size: 14px !important;
        margin-top: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .section {
        margin-top: 36px !important;
    }
    
    /* Enhanced DataFrame styling */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px rgba(220, 38, 38, 0.08) !important;
    }
    
    [data-testid="stDataFrame"] {
        color: #1a1a1a !important;
    }
    
    thead tr th {
        color: #1a1a1a !important;
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%) !important;
        font-weight: 700 !important;
        padding: 16px !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        letter-spacing: 0.8px !important;
        border-bottom: 2px solid #fca5a5 !important;
    }
    
    tbody tr td {
        color: #334155 !important;
        padding: 14px 16px !important;
        border-bottom: 1px solid rgba(220, 38, 38, 0.05) !important;
    }
    
    tbody tr:hover {
        background: rgba(220, 38, 38, 0.02) !important;
        transition: background 0.2s ease !important;
    }
    
    /* Sidebar premium styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 241, 242, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(220, 38, 38, 0.15) !important;
        box-shadow: 4px 0 24px rgba(220, 38, 38, 0.08) !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #dc2626 !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #334155 !important;
    }
    
    /* Modern file uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px dashed #fca5a5 !important;
        border-radius: 20px !important;
        padding: 40px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #dc2626 !important;
        background: rgba(255, 245, 245, 0.8) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 12px 40px rgba(220, 38, 38, 0.12) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* Premium button styling */
    .stButton button {
        background: linear-gradient(135deg, #dc2626 0%, #e11d48 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 36px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 12px 32px rgba(220, 38, 38, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 16px 48px rgba(220, 38, 38, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Animated spinner */
    .stSpinner > div {
        border-top-color: #dc2626 !important;
        border-width: 3px !important;
    }
    
    /* Enhanced info box */
    .stInfo {
        background: linear-gradient(135deg, rgba(255, 241, 242, 0.8) 0%, rgba(255, 255, 255, 0.8) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-left: 5px solid #dc2626 !important;
        border-radius: 16px !important;
        color: #1a1a1a !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px rgba(220, 38, 38, 0.1) !important;
    }
    
    /* Card headers with icon space */
    .card h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
        margin-bottom: 1.8rem !important;
        padding-bottom: 12px !important;
        border-bottom: 2px solid rgba(220, 38, 38, 0.1) !important;
    }
    
    /* Smooth scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 241, 242, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #fca5a5 0%, #dc2626 100%);
        border-radius: 10px;
        transition: background 0.3s;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #dc2626 0%, #be123c 100%);
    }
</style>
""", unsafe_allow_html=True)

#LOGIC
def file_loader(source_type, source, **kwargs):
    if source_type == 'csv':
        df = pd.read_csv(source)

    elif source_type == 'excel':
        sheet = kwargs.get('sheet', 0)
        df = pd.read_excel(source, sheet_name=sheet)

    elif source_type == 'json':
        df = pd.read_json(source)

    elif source_type == 'sql':
        engine = create_engine(source)
        query = kwargs.get("query")
        df = pd.read_sql(query, engine)

    else:
        raise ValueError("Invalid source type")

    return df


def data_summary(df):
    return {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'column_names': list(df.columns),
        'unique_values': df.nunique().to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.astype(str).to_dict(),
        'statistical_summary': df.describe(include='all').to_dict()
    }

# SIDEBAR 
st.sidebar.markdown("## 🔴 Data Analyzer Platform")
st.sidebar.markdown(
    "<span style='color:#334155; font-weight:600; font-size:15px'>Professional dataset analysis and profiling tool</span>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Supported Formats**")
st.sidebar.write("📊 CSV Files")
st.sidebar.write("📈 Excel Workbooks")
st.sidebar.write("📋 JSON Documents")

# MAIN HEADER 
st.markdown("# Dataset Overview")
st.markdown(
    "<div class='subtitle'>Understand your dataset in seconds.</div>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "json"]
)

if uploaded_file:
    with st.spinner("Analyzing your dataset..."):

        name = uploaded_file.name.lower()

        if name.endswith(".csv"):
            df = file_loader("csv", uploaded_file)

        elif name.endswith(".xlsx"):
            df = file_loader("excel", uploaded_file)

        elif name.endswith(".json"):
            df = file_loader("json", uploaded_file)

        else:
            st.error("Unsupported file format")
            st.stop()

        summary = data_summary(df)

    #METRICS
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            f"""
            <div class="metric">
                <h1>{summary['rows']:,}</h1>
                <p>Total Rows</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric">
                <h1>{summary['columns']}</h1>
                <p>Total Columns</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric">
                <h1>{len(df.select_dtypes(include='number').columns)}</h1>
                <p>Total Numerical Columns</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # SCHEMA 
    st.markdown("<div class='section card'>", unsafe_allow_html=True)
    st.markdown("### Schema & Data Types")
    st.dataframe(
        pd.DataFrame.from_dict(
            summary["data_types"],
            orient="index",
            columns=["Data Type"]
        ),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # DATA QUALITY 
    st.markdown("<div class='section card'>", unsafe_allow_html=True)
    st.markdown("### ✓ Data Quality Report")
    st.dataframe(
        pd.DataFrame.from_dict(
            summary["missing_values"],
            orient="index",
            columns=["Missing Values"]
        ),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # STATISTICS
    st.markdown("<div class='section card'>", unsafe_allow_html=True)
    st.markdown("### Statistical Summary")
    st.dataframe(
        pd.DataFrame(summary["statistical_summary"]),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # PREVIEW 
    st.markdown("<div class='section card'>", unsafe_allow_html=True)
    st.markdown("### Data Preview")
    st.dataframe(df.head(25), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:

    st.info("📤 Upload a dataset to begin your analysis journey.")




