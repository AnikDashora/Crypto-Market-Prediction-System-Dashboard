import streamlit as st
import os 
import sys
from streamlit_echarts import st_echarts
import pandas as pd
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from datahandeling_and_other.helper import format_usd,build_growth_comparison_bar_option,build_normalized_price_index_option

names = [
    "Bitcoin",
    "Rain",
    "Monero",
    "Mantle",
    "Canton",
    "Wrapped Beacon ETH"
]

growth_30d = [
    4.7937,
    109.4092,
    36.5346,
    21.8719,
    13.2347,
    10.9487
]

option = {
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"}
    },
    "grid": {
        "left": "5%",
        "right": "5%",
        "bottom": "10%",
        "containLabel": True
    },
    "xAxis": {
        "type": "category",
        "data": names,
        "axisLabel": {
            "rotate": 30
        }
    },
    "yAxis": {
        "type": "value",
        "name": "Growth %"
    },
    "series": [
        {
            "name": "Growth 30D",
            "type": "bar",
            "data": [
                {
                    "value": v,
                    "itemStyle": {
                        "color": "#16a34a" if v >= 0 else "#dc2626"
                    }
                }
                for v in growth_30d
            ],
            "barWidth": "50%",
            "label": {
                "show": True,
                "position": "top",
                "formatter": "{c}%"
            }
        }
    ]
}

coins = [
    "Bitcoin",
    "Rain",
    "Monero",
    "Mantle",
    "Canton",
    "Wrapped Beacon ETH"
]

growth_30d = [
    4.7937,
    109.4092,
    36.5346,
    21.8719,
    13.2347,
    10.9487
]


series = [
    {
        "name": coin,
        "type": "line",
        "data": [value],
        "symbol": "circle",
        "symbolSize": 10,
        "lineStyle": {"width": 3}
    }
    for coin, value in zip(coins, growth_30d)
]

option1 = {
    "tooltip": {
        "trigger": "axis"
    },
    "legend": {
        "right": "3%",
        "type": "scroll"
    },
    "grid": {
        "left": "5%",
        "right": "5%",
        "bottom": "10%",
        "containLabel": True
    },
    "xAxis": {
        "type": "category",
        "data": ["30 Days"]
    },
    "yAxis": {
        "type": "value"
    },
    "series": series
}

from session_state.session_manager import to_classification_page,to_ml_page,to_growth_page,to_verdict_page,to_investment_page,to_overview_page
remove_header_footer = """
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Hide the orange loading progress bar */
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    .stDeployButton{
        display:none;
    }
    /* Remove top padding to avoid white space */
    .block-container {
        padding-top: 1rem !important;
    }
"""

page_setup = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            gap:0;
        }

        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #f59e0b;
            --accent: #06d6a0;
            --background: #fefefe;
            --card: #ffffff;
            --text-primary: #1a1a1a;
            --text-secondary: #6b7280;
            --border: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --radius: 12px;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
        }

        html {
            font-size: var(--font-size);
        }
        

            /* Main Streamlit App Container */
            .stApp {
                min-height: 100vh !important;
                display: flex !important;
                flex-direction: column !important;
                background: var(--background) !important;
                padding: var(--page-padding);
                box-sizing: border-box;
            }

            /* Main View Container */
            .stAppViewContainer {
                flex: 1 1 auto !important;
                max-width: var(--max-width);
                margin: 0 auto;
                width: 100%;
                background: transparent !important;
                padding: 0 !important;
                display: flex;
                flex-direction: column;
                gap: 2.5rem;
                
            }

            /* Main Block Container */
            .stMainBlockContainer {
                background: transparent !important;
                padding: 0 !important;
                width: 1440px;
                max-width: var(--max-width) !important;
                margin: 0 auto;
                flex: 1 1 auto !important;
                display: flex !important;
                flex-direction: column !important;
                gap: 2rem;
            }

            /* In the Main container inside MainBlockContainer */
            .stMain .stMainBlockContainer {
                padding: 0 !important;
                margin: 0 auto;
                
                
            }

            /* Vertical block (commonly for rows of content) */
            

            /* Remove default top padding for block container (as per your remove_header_footer style) */
            .block-container {
                padding-top: 1rem !important;
            }

            .stMainBlockContainer .st-emotion-cache-8fjoqp{
                gap:0rem;
            } 
            
        

        
"""

navbar_styles = """
/* ================================
   NAVBAR WRAPPER
================================ */
.st-key-navbar {
    background: var(--card);
    box-shadow: var(--shadow);
    padding: 1rem 0;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid var(--border);
    position: sticky;
    width: 100%;
}

/* ================================
   NAV CONTAINER
================================ */
.st-key-nav-container {
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    width: 100%;
    max-width: 2000px;
}

/* ================================
   LOGO
================================ */
.logo {
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary);
    text-decoration: none;
    letter-spacing: -0.02em;
    flex-shrink: 0;
    user-select: none;
    transition: color 0.2s;
}

/* ================================
   STREAMLIT COLUMN FIX
================================ */
.st-key-navbar .st-emotion-cache-ko87jo {
    display: flex;
    align-items: center;
}


/* ================================
   NAV BUTTONS CONTAINER
================================ */
.st-key-nav-buttons {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Streamlit horizontal block fix */
.st-key-nav-buttons .stHorizontalBlock {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* ================================
   BUTTON BASE STYLE
================================ */
.st-key-nav-buttons .stButton {
    display: flex;
    align-items: center;
}

.st-key-nav-buttons .stButton button {
    min-width: 140px;
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;

    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: #ffffff;
    color: var(--text-primary);

    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;

    outline: none;
    overflow: hidden;
    white-space: nowrap;
}

/* ================================
   BUTTON HOVER
================================ */
.st-key-nav-buttons .stButton button:hover,
.st-key-nav-buttons .stButton button:focus-visible {
    background: var(--primary);
    color: #ffffff;
    transform: translateY(-2px) scale(1.03);
    box-shadow: var(--shadow);
}

/* ================================
   PRIMARY CTA BUTTON
================================ */
.st-key-nav-btn-3 .stButton button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-3 .stButton button:hover,
.st-key-nav-btn-3 .stButton button:focus-visible {
    background: linear-gradient(135deg, var(--primary-dark), #3730a3);
}

/* ================================
   TEXT FIX
================================ */
.st-key-nav-buttons .stButton button p {
    margin: 0;
}
/* ================================
   NAV BUTTONS – ROOT FIX
================================ */
.st-key-nav-buttons {
    display: flex !important;
    align-items: center;
    justify-content: flex-end;
    gap: 0.75rem;
    width: 100%;
}

/* Remove Streamlit column shrink issues */
.st-key-nav-buttons .stColumn {
    width: auto !important;
    flex: 0 0 auto !important;
}

/* Horizontal row */
.st-key-nav-buttons .stHorizontalBlock {
    display: flex !important;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: nowrap;
}

/* ================================
   BUTTON BASE
================================ */
.st-key-nav-buttons .stButton button {
    min-width: 150px;          /* uniform width */
    height: 42px;

    padding: 0 1.25rem;
    border-radius: 999px;     /* pill shape */
    border: 1px solid var(--border);

    background: #ffffff;
    color: var(--text-primary);

    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.2px;

    display: flex;
    align-items: center;
    justify-content: center;

    white-space: nowrap;
    cursor: pointer;

    transition:
        background 0.25s ease,
        color 0.25s ease,
        transform 0.2s ease,
        box-shadow 0.25s ease;
}

/* ================================
   HOVER EFFECT
================================ */
.st-key-nav-buttons .stButton button:hover {
    background: var(--primary);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 6px 15px rgba(99, 102, 241, 0.25);
}

/* ================================
   ACTIVE / SELECTED BUTTON
   (you can toggle this class in Python)
================================ */
.st-key-nav-buttons .active-nav button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
}

/* ================================
   CTA / IMPORTANT BUTTON
================================ */
.st-key-nav-btn-4 .stButton button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-4 .stButton button:hover {
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 10px 24px rgba(99, 102, 241, 0.4);
}

/* ================================
   TEXT FIX
================================ */
.st-key-nav-buttons .stButton p {
    margin: 0;
    line-height: 1;
}
.stMainBlockContainer .st-emotion-cache-tn0cau{
    gap:0rem;
}

.st-key-nav-container .stHorizontalBlock{
                display:flex;
                align-items:center;
                justify-content:space-around;
}
     

"""

cart_header_style = """
        .st-key-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .st-key-cart-header {
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            flex-direction: row;
            gap:10rem;
        }

        .st-key-back-button {
            margin-bottom: 1rem;
            max-width:200px;
            width:100%;
            flex-wrap:wrap;
        }

        .st-key-back-button .stButton button {
            width:100%;
            background: transparent;
            border: none;
            border-radius: var(--radius);
            padding: 0.75rem 1rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .st-key-back-button .stButton button:hover {
            color: var(--primary-dark);
            background-color: rgba(99, 102, 241, 0.2);
        }

        .cart-title-section .page-title {
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }

        .cart-title-section .item-count {
            color: var(--text-secondary);
            font-size: 2rem;
        }
"""

kpi_styles = """
        [class *= "st-key-kpi-grid"] {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin: 30px 0;
        }
        /* IMPORTANT: fix Streamlit wrappers */
        [class *= "st-key-kpi-grid"] > div {
            display: contents;
        }

        [class *= "st-key-kpi-card"] {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        }

        [class *= "st-key-kpi-card"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        [class *= "st-key-kpi-card"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
        }

        [class *= "st-key-kpi-card"]:hover::before {
            opacity: 1;
        }

        .kpi-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .kpi-title {
            font-size: 0.9rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .kpi-icon {
            width: 24px;
            height: 24px;
            opacity: 0.7;
            color: #3b82f6;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #1e293b;
            animation: fadeInUp 0.6s ease;
        }

        .kpi-change {
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 5px;
            font-weight: 500;
        }

        .positive { color: #16a34a; }
        .negative { color: #dc2626; }
        .neutral { color: #64748b; }


"""
card_styles = """
        /* Card Styles */
        .card {
            background: white;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }

        .card-header {
            padding: 1.5rem;
            border-bottom: 1px solid #e2e8f0;
        }

        .card-header.gradient {
            background: linear-gradient(90deg, #f8fafc, #eff6ff);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-description {
            font-size: 0.875rem;
            color: #64748b;
        }

        .card-content {
            padding: 1.5rem;
        }

        .card-content.no-padding {
            padding: 0;
        }
         /* Verdict Grid */
        .verdict-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }

        .verdict-card {
            border-left: 4px solid #dc2626;
        }

        .confidence-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .confidence-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }

        .confidence-fill.green {
            background: linear-gradient(90deg, #16a34a, #10b981);
        }

        .confidence-fill.red {
            background: #dc2626;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 1.5rem;
            text-align: center;
        }

        .metric-label {
            font-size: 0.75rem;
            color: #64748b;
            margin-bottom: 0.25rem;
        }

        .metric-value {
            font-weight: 600;
            color: #1e293b;
        }

        .metric-value.green { color: #16a34a; }
        .metric-value.orange { color: #ea580c; }

        .verdict-list {
            margin-top: 1rem;
        }

        .verdict-list p {
            font-size: 0.875rem;
            color: #475569;
            margin-bottom: 0.5rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
        }

        .badge.success {
            background: linear-gradient(90deg, #16a34a, #10b981);
            color: white;
        }

        .badge.danger {
            background: #dc2626;
            color: white;
        }
"""
table_styles = """
        .table-container {
            overflow-y: auto;
            max-height: 500px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table thead {
            position: sticky;
            top: 0;
            z-index: 10;
            background: #f1f5f9;
        }

        .data-table th {
            padding: 1rem;
            text-align: left;
            font-weight: 700;
            color: #475569;
            border-bottom: 2px solid #cbd5e1;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .data-table th.text-right {
            text-align: right;
        }

        .data-table tbody tr {
            border-bottom: 1px solid #e2e8f0;
            transition: all 0.2s;
        }

        .data-table tbody tr:nth-child(even) {
            background: rgba(248, 250, 252, 0.5);
        }

        .data-table tbody tr:hover {
            background: #eff6ff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .data-table td {
            padding: 1rem;
            font-size: 0.875rem;
        }

        .index-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #e2e8f0;
            color: #475569;
            font-weight: 600;
            font-size: 0.875rem;
        }

        .date-cell {
            font-family: 'Courier New', monospace;
            color: #475569;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .date-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #3b82f6;
        }

        .price-cell {
            text-align: right;
            font-family: 'Courier New', monospace;
            font-size: 1.125rem;
            font-weight: 600;
            color: #1e293b;
        }

        .icon-badge {
            width: 32px;
            height: 32px;
            background: #3b82f6;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
"""

chart_styles = """
        [class *= "st-key-card-"] {
            background: white;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }
        .st-key-card-3{
        margin-bottom: 2rem;
        }
        .card-header {
            padding: 1.5rem;
            border-bottom: 1px solid #e2e8f0;
        }

        .card-header.gradient {
            background: linear-gradient(90deg, #f8fafc, #eff6ff);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-description {
            font-size: 0.875rem;
            color: #64748b;
        }

        [class *= "st-key-card-content"] {
            padding: 1.5rem;
        }

        .card-content.no-padding {
            padding: 0;
        }

        /* Charts Grid */
        .st-key-chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
            margin-top:2rem;
        }

        [class *= "st-key-chart-container"] {
            height: 320px;
            position: relative;
        }

        [class *= "st-key-chart-container-large-"] {
            height: 384px;
            position: relative;
        }

"""


styles = f"""
    <style>
    {remove_header_footer}
    {page_setup}
    {navbar_styles}
    {kpi_styles}
    {card_styles}
    {chart_styles}
    {table_styles}
    </style>
"""

def investment_page():
    st.set_page_config(
        page_title="Overview",
        page_icon="",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown(styles,unsafe_allow_html=True)
    with st.container(key = "navbar"):
        with st.container(key = "nav-container"):
                with st.container(key = "nav-buttons"):
                    overview_col,ml_col,classification_col,investment_col,verdict_col = st.columns(5)
                    
                    with overview_col:
                        st.button(
                            label="Overview",
                            key = "nav-btn-1",
                            type="secondary",
                        )
                    with ml_col:
                        st.button(
                            label="ML Prediction",
                            key = "nav-btn-2",
                            type="secondary",
                            on_click=to_ml_page
                        )
                    with classification_col:
                        st.button(
                            label="Classification",
                            key = "nav-btn-3",
                            type="secondary",
                            on_click=to_classification_page
                        )
                    with investment_col:
                        st.button(
                            label="Investment",
                            key = "nav-btn-4",
                            type="secondary",
                            on_click=to_investment_page
                        )
                    with verdict_col:
                        st.button(
                            label="AI Verdict",
                            key = "nav-btn-6",
                            type="secondary",
                            on_click=to_verdict_page
                        )
    st.markdown(
            """
            <div class="section-header">
                <h2>Investment Return Simulator — 6 Months Back</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with st.container(key = "kpi-grid-1"):
        
        with st.container(key = "kpi-card-1"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Investment Amount</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                        <path d="M2 17l10 5 10-5"></path>
                        <path d="M2 12l10 5 10-5"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(st.session_state["investment_amount"] )}</div>
                <div class="kpi-change positive">
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-2"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Coins Bought (approx.)</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 3v16a2 2 0 0 0 2 2h16"></path>
                        <path d="M18 17V9"></path>
                        <path d="M13 17V5"></path>
                        <path d="M8 17v-3"></path>
                    </svg>
                </div>
                <div class="kpi-value">{st.session_state["investment_result"]['coins_bought']:.4f}</div>
                <div class="kpi-change positive">
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-3"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Current Value</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 7h6v6"></path>
                        <path d="m22 7-8.5 8.5-5-5L2 17"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(st.session_state["investment_result"]["current_value"])}</div>
                <div class="kpi-change negative">
                </div>
            """,unsafe_allow_html=True)
        
        with st.container(key = "kpi-card-4"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">ROI %</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path>
                    </svg>
                </div>
                <div class="kpi-value">{st.session_state["investment_result"]['roi_percent']:.2f}%</div>
                <div class="kpi-change neutral">
                </div>
            """,unsafe_allow_html=True)
    st.markdown(
            """
            <div class="section-header">
                <h2>Predicted Investment Outcome — Next 6 Months (ML Based)</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with st.container(key = "kpi-grid-2"):
        coins_bought_today = st.session_state["investment_amount"] / st.session_state["current_price"] if st.session_state["current_price"] > 0 else 0.0
        future_6m_price = None
        if "6 Months" in  st.session_state["future_predictions"]:
            future_6m_price =  st.session_state["future_predictions"]["6 Months"].get("Multiple Linear")
        future_value = coins_bought_today * future_6m_price

        future_profit_loss = future_value - st.session_state["investment_amount"]

        future_roi = (future_profit_loss / st.session_state["investment_amount"]) * 100 if st.session_state["investment_amount"] > 0 else 0.0
        with st.container(key = "kpi-card-5"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Coins Bought Today</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                        <path d="M2 17l10 5 10-5"></path>
                        <path d="M2 12l10 5 10-5"></path>
                    </svg>
                </div>
                <div class="kpi-value">{coins_bought_today:.6f}</div>
                <div class="kpi-change positive">
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-6"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Predicted Price (6M)</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 3v16a2 2 0 0 0 2 2h16"></path>
                        <path d="M18 17V9"></path>
                        <path d="M13 17V5"></path>
                        <path d="M8 17v-3"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(future_6m_price)}</div>
                <div class="kpi-change positive">
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-7"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Predicted Value (6M)</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 7h6v6"></path>
                        <path d="m22 7-8.5 8.5-5-5L2 17"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(future_value)}</div>
                <div class="kpi-change negative">
                </div>
            """,unsafe_allow_html=True)
        
        with st.container(key = "kpi-card-8"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Predicted ROI %</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path>
                    </svg>
                </div>
                <div class="kpi-value">{future_roi:.2f}%</div>
                <div class="kpi-change neutral">
                </div>
            """,unsafe_allow_html=True)

    

    st.markdown(
            """
            <div class="section-header">
                <h2>Top 5 Fastest Growing Coins (Last 30 Days)</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.session_state["top_growth_df"]
    selected_30d_growth = None
    if "prices" in st.session_state["market_chart"]:
        df_hist_30 = st.session_state["df_daily"].sort_values("date")
        cutoff_30 = df_hist_30["date"].max() - pd.Timedelta(days=30)
        df_30 = df_hist_30[df_hist_30["date"] >= cutoff_30]
        if len(df_30) > 1:
            p_start = df_30["price"].iloc[0]
            p_end = df_30["price"].iloc[-1]
            if p_start > 0:
                selected_30d_growth = ((p_end - p_start) / p_start) * 100.0

    comp_rows = []
    if selected_30d_growth is not None:
        comp_rows.append(
        {
            "id": st.session_state["coin_id"],
            "name": st.session_state["coin_overview"].get("name", st.session_state["coin_id"]),
            "growth_30d": selected_30d_growth,
        }
        )
    comp_rows.extend(
                [
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "growth_30d": row["growth_30d"],
                    }
                    for _, row in st.session_state["top_growth_df"].iterrows()
                ]
            )
    comp_df = pd.DataFrame(comp_rows)

    with st.container(key = "chart-grid"):
        with st.container(key = "card-1"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Price Movement (24h)</div>
                    <div class="card-description">Real-time price tracking with volume indicators</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-1"):
                with st.container(key = "chart-container-1"):
                    st_echarts(build_growth_comparison_bar_option(comp_df))

        
        with st.container(key = "card-2"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Price Movement (24h)</div>
                    <div class="card-description">Real-time price tracking with volume indicators</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-2"):
                with st.container(key = "chart-container-2"):
                    st_echarts(build_normalized_price_index_option(st.session_state["comparative_history"],st.session_state["coin_id"]))
   
    price_df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
        "Close": [100, 102, 101, 105, 108, 107, 110, 112, 111, 115]
    })
    table = []

    for index, row in price_df.iterrows():
        date = row["Date"].strftime("%Y-%m-%d")
        price = f"${row['Close']:,}"
        table.append(f'<tr><td><span class="index-badge">{index + 1}</span></td><td><div class="date-cell"><div class="date-dot"></div>{date}</div></td><td class="price-cell">{price}</td></tr>')
    
    st.markdown(
        f"""
            <div class="card" style="margin-top: 2rem;">
                <div class="card-header gradient">
                    <div class="card-title">
                        <span class="icon-badge">
                            <i class="fas fa-table"></i>
                        </span>
                        Dataframe (Daily Closing Prices)
                    </div>
                    <div class="card-description">Historical daily closing price data</div>
                </div>
                <div class="card-content no-padding">
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th style="width: 120px;">Index</th>
                                    <th>Date</th>
                                    <th class="text-right">Close Price (USD)</th>
                                </tr>
                            </thead>
                            <tbody id="priceTableBody">
                               {"".join(table)}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )
