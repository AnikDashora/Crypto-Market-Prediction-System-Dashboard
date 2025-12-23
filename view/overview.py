import streamlit as st
import os 
import sys
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from datahandeling_and_other.helper import format_usd,format_volume,build_market_cap_line_option,build_volume_bar_option,build_price_ema_line_option

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
.st-key-nav-btn-1 .stButton button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-1 .stButton button:hover {
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
        .st-key-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin: 30px 0;
        }
        /* IMPORTANT: fix Streamlit wrappers */
        .st-key-kpi-grid > div {
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

kpi_card_3_style = """
.st-key-kpi-card-3 {
    grid-column: span 2;
    grid-row: span 2;
}
.st-key-kpi-card-3 .kpi-header {
    display: flex;
    flex-direction: column;     /* COLUMN layout */
    align-items: flex-start;    /* left aligned */
    gap: 0.4rem;
}
.st-key-kpi-card-3 .card-description {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.4;
}
.st-key-kpi-card-3::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 0px;
    background: none;
    opacity: 0;
    transition: opacity 0.3s ease;
}
"""
kpi_card_4_style ="""
.st-key-kpi-card-4 {
    grid-column: span 2;
    grid-row: span 2;
}
.st-key-kpi-card-4 .kpi-header {
    display: flex;
    flex-direction: column;     /* COLUMN layout */
    align-items: flex-start;    /* left aligned */
    gap: 0.4rem;
}
.st-key-kpi-card-4 .card-description {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.4;
}
.st-key-kpi-card-4::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 0px;
    background: none;
    opacity: 0;
    transition: opacity 0.3s ease;
}
"""

kpi_card_4_style_positive = """
.st-key-kpi-card-4 {
    border-right:4px solid #16a34a;
}
.st-key-kpi-card-4:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(22, 163, 74, 0.25);
}
"""
kpi_card_4_style_neutral = """
.st-key-kpi-card-4 {
    border-right:4px solid #64748b;
}
.st-key-kpi-card-4:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(100, 116, 139, 0.22);
}
"""
kpi_card_4_style_negative = """
.st-key-kpi-card-4 {
    border-right:4px solid #dc2626;
}
.st-key-kpi-card-4:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(220, 38, 38, 0.25);
}
"""

kpi_card_3_style_positive = """
.st-key-kpi-card-3 {
    border-left:4px solid #16a34a;
}
.st-key-kpi-card-3:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(22, 163, 74, 0.25);
}
"""
kpi_card_3_style_neutral = """
.st-key-kpi-card-3 {
    border-left:4px solid #64748b;
}
.st-key-kpi-card-3:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(100, 116, 139, 0.22);
}
"""
kpi_card_3_style_negative = """
.st-key-kpi-card-3 {
    border-left:4px solid #dc2626;
}
.st-key-kpi-card-3:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(220, 38, 38, 0.25);
}
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

        .confidence-fill.neutral {
            background: #64748b;
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
        .badge.neutral{
            background: #64748b;
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
        }

        [class *= "st-key-chart-container"] {
            height: 320px;
            position: relative;
        }

        .st-key-chart-container-large {
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
    {kpi_card_3_style}
    {kpi_card_4_style}
    {kpi_card_3_style_negative}
    {kpi_card_4_style_positive}
    {card_styles}
    {table_styles}
    {chart_styles}
    </style>
"""

def overview_page():
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

    with st.container(key = "kpi-grid"):
        with st.container(key = "kpi-card-1"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Current Price</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                        <path d="M2 17l10 5 10-5"></path>
                        <path d="M2 12l10 5 10-5"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(st.session_state["current_price"])}</div>
                <div class="kpi-change negative">
                    <span>↗</span> +$2.45 (1.36%)
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-2"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Total Volume</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 3v16a2 2 0 0 0 2 2h16"></path>
                        <path d="M18 17V9"></path>
                        <path d="M13 17V5"></path>
                        <path d="M8 17v-3"></path>
                    </svg>
                </div>
                <div class="kpi-value">{format_volume(st.session_state["total_volume"])}</div>
                <div class="kpi-change positive">
                    <span>↗</span> +12.5% vs avg volume
                </div>
            """,unsafe_allow_html=True)
        if(st.session_state["final_verdict"]["verdict"] == "BUY"):
            verdict_trend_badge = "success"
            verdict_trend_text_color = "#16a34a"
            verdict_confidance_fill_color = "green"
        elif(st.session_state["final_verdict"]["verdict"] == "AVOID"):
            verdict_trend_badge = "danger"
            verdict_trend_text_color = "#dc2626"
            verdict_confidance_fill_color = "red"
        else:
            verdict_trend_badge = "neutral"
            verdict_trend_text_color = "#64748b"
            verdict_confidance_fill_color = "neutral"
        with st.container(key = "kpi-card-3"):
            st.markdown(f"""
                <div class="card-header">
                    <div class="card-title">Short Verdict</div>
                    <div class="card-description">Based on: Regression trend, ML trend classification, news sentiment, and historical ROI simulation</div>
                    
                </div>
                <div class="card-content">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                            <span class="badge {verdict_trend_badge}">{st.session_state["final_verdict"]["verdict"]}</span>
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-bottom: 0.5rem;">
                                    <span style="color: #64748b;">Confidence Level</span>
                                    <span style="color: {verdict_trend_text_color}; font-weight: 600;">{int(st.session_state["final_verdict"]['confidence'])}%</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill {verdict_confidance_fill_color}" style="width: {int(st.session_state["final_verdict"]['confidence'])}%;"></div>
                                </div>
                            </div>
                        </div>
                        <div class="verdict-list">
                            <p>• High volatility detected in short-term patterns</p>
                            <p>• Mixed signals from technical indicators</p>
                        </div>
                    </div>
            """,unsafe_allow_html=True)
        if(st.session_state["trend_majority"][0] == "Bullish"):
            trend_badge = "success"
            trend_text_color = "#16a34a"
            trend_confidance_fill_color = "green"
        else:
            trend_badge = "danger"
            trend_text_color = "#dc2626"
            trend_confidance_fill_color = "red"
        macd = round(np.nanmean(st.session_state["df_daily"]["macd"]),3)
        if(macd < 0):
            color = "orange"
        else:
            color = "green"
        with st.container(key = "kpi-card-4"):
            st.markdown(f"""
                <div class="card-header">
                        <div class="card-title">Trend Snapshot</div>
                        <div class="card-description">Trend (Model Majority)</div>
                    </div>
                    <div class="card-content">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                            <span class="badge {trend_badge}">{st.session_state["trend_majority"][0]}</span>
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-bottom: 0.5rem;">
                                    <span style="color: #64748b;">{st.session_state["trend_majority"][0]} Confidence</span>
                                    <span style="color: {trend_text_color}; font-weight: 600;">{int(st.session_state["trend_majority"][1])}%</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill {trend_confidance_fill_color}" style="width: {int(st.session_state["trend_majority"][1])}%;"></div>
                                </div>
                            </div>
                        </div>
                        <div class="metrics-grid">
                            <div>
                                <div class="metric-label">RSI (14)</div>
                                <div class="metric-value">{round(np.nanmean(st.session_state["df_daily"]["rsi_14"]),3)}</div>
                            </div>
                            <div>
                                <div class="metric-label">MACD</div>
                                <div class="metric-value {color}">{macd}</div>
                            </div>
                        </div>
                    </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-5"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">EMA 10</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                        <line x1="9" y1="9" x2="9.01" y2="9"></line>
                        <line x1="15" y1="9" x2="15.01" y2="9"></line>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(np.sum(st.session_state["df_daily"]["ema_10"]))}</div>
                <div class="kpi-change positive">
                    <span>↗</span> Above EMA
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-6"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">SMA 9 EMA</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 9V5a3 3 0 0 0-6 0v4"></path>
                        <rect x="2" y="9" width="20" height="11" rx="2" ry="2"></rect>
                    </svg>
                </div>
                <div class="kpi-value">{format_usd(np.sum(st.session_state["df_daily"]["sma_9_ema"]))}</div>
                <div class="kpi-change positive">
                    <span>↗</span> Bullish
                </div>
            """,unsafe_allow_html=True)
        
    with st.container(key = "chart-grid"):
        with st.container(key = "card-1"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Last 30D Market CAP)</div>
                    <div class="card-description">Real-time Market tracking</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-1"):
                with st.container(key = "chart-container-1"):
                    st_echarts(build_market_cap_line_option(st.session_state["df_daily"]))
        with st.container(key = "card-2"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Last 7 Days Volume</div>
                    <div class="card-description">Real-time tracking of volume indicators</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-2"):
                with st.container(key = "chart-container-2"):
                    st_echarts(build_volume_bar_option(st.session_state["df_daily"]))
                    
    with st.container(key = "card-3"):
        st.markdown(
            """
            <div class="card-header">
                <div class="card-title">Market Trend Analysis</div>
                <div class="card-description">Price movement with moving averages and Close Price</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.container(key = "card-content-3"):
            with st.container(key = "chart-container-large"):
                st_echarts(build_price_ema_line_option(st.session_state["df_daily"]))
                # pass
    
    price_df = st.session_state["df_daily"].head(15)

    table = []

    for index, row in price_df.iterrows():
        date = row["date"].strftime("%Y-%m-%d")
        price = f"{format_usd(row['price'])}"
        table.append(f'<tr><td><span class="index-badge">{index + 1}</span></td><td><div class="date-cell"><div class="date-dot"></div>{date}</div></td><td class="price-cell">{price}</td></tr>')

    st.markdown(
        f"""
            <div class="card" style="margin-top: 2rem;">
                <div class="card-header gradient">
                    <div class="card-title">
                        <span class="icon-badge">
                            <i class="fas fa-table"></i>
                        </span>
                        Daily Closing Prices
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

        
