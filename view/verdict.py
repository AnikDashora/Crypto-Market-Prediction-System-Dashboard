import streamlit as st
import os 
import sys
import pandas as pd
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from session_state.session_manager import to_classification_page,to_ml_page,to_growth_page,to_verdict_page,to_investment_page,to_overview_page

def get_score_type(score):
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

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
.st-key-nav-btn-6 .stButton button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-6 .stButton button:hover {
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

cart_button_styles = """
        [class *= "st-key-item-controls-"]{
            display: flex;
            align-items: center;
            justify-content:space-around;
            flex-direction: row;
            width:100%;
        }
        [class *= "st-key-quantity-controls-"] {
            display: flex;
            align-items: center;
            justify-content:center;
            flex-direction: row;
            gap: 0.5rem;
            background: rgba(99, 102, 241, 0.2);
            border-radius: 50px;
            padding: 0.25rem;
            width: fit-content;
            border:1px solid var(--border);
            width:100%;
        }

        [class *= "st-key-quantity-controls-"] div[data-testid="stMarkdownContainer"]{
            margin-bottom:0rem;
        }

        [class *= "st-key-minus-btn-"] .stButton button,
        [class *= "st-key-plus-btn-"] .stButton button {
            display:flex;
            align-items:center;
            justify-content:center;
            width: 2.5rem;
            height: 2.5rem;
            border: none;
            background: var(--primary);
            color: white;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1.1rem;
            transition: background 0.2s;
        }

        [class *= "st-key-minus-btn-"] .stButton button:hover,
        [class *= "st-key-plus-btn-"] .stButton button:hover {
            background: var(--primary-dark);
        }

        .quantity-display {
            display:flex;
            align-items:center;
            justify-content:center;
            min-width: 100%;
            height:40px;
            text-align: center;
            border:none;
            font-weight: 600;
            font-size: 1rem;
            background-color: transparent;
            width: fit-content;
        }

"""

page_style = """
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        }

        body {
        font-family:
            -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
            "Helvetica Neue", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        }

        .app {
        min-height: 100vh;
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eff6ff 50%,
            #f1f5f9 100%
        );
        padding: 2rem;
        }

        .st-key-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            margin-top:2rem;
        }

        body {
        font-family:
            -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
            "Helvetica Neue", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        }
        

        

        /* Verdict Card */
        .verdict-card {
        background: white;
        border-radius: 1rem;
        border: 2px solid;
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        overflow: hidden;
        }

        .verdict-card.avoid {
        background: #fef2f2;
        border-color: #fecaca;
        }

        .verdict-card.buy {
        background: #f0fdf4;
        border-color: #bbf7d0;
        }

        .verdict-card.hold {
        background: #fefce8;
        border-color: #fde68a;
        }

        .verdict-content {
        padding: 2rem;
        display: flex;
        gap: 1.5rem;
        align-items: center;
        }

        .verdict-icon {
        width: 5rem;
        height: 5rem;
        border-radius: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .verdict-icon.avoid {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }

        .verdict-icon.buy {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        }

        .verdict-icon.hold {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        }

        .verdict-icon svg {
        width: 2.5rem;
        height: 2.5rem;
        color: white;
        }

        .verdict-details {
        flex: 1;
        }

        .verdict-header {
        display: flex;
        align-items: baseline;
        gap: 1rem;
        margin-bottom: 0.5rem;
        }

        .verdict-title {
        font-size: 3rem;
        font-weight: 700;
        }

        .verdict-title.avoid {
        color: #b91c1c;
        }

        .verdict-title.buy {
        color: #15803d;
        }

        .verdict-title.hold {
        color: #a16207;
        }

        .verdict-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.875rem;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        background: white;
        }

        .verdict-description {
        color: #64748b;
        margin-bottom: 1rem;
        }

        .confidence-section {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        }

        .confidence-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.875rem;
        color: #64748b;
        }

        .progress-bar {
        width: 100%;
        height: 0.75rem;
        background: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
        }

        .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 9999px;
        transition: width 0.5s ease;
        }
        .progress-fill.avoid{
            background:#b91c1c;
        }
        .progress-fill.buy{
            background:#15803d;
        }
        .progress-fill.hold{
            background:#a16207;
        }

        /* Card */
        .card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        .card-header {
        padding: 1.5rem;
        border-bottom: 1px solid #f1f5f9;
        }

        .header-icon-wrapper {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        }

        .header-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        }

        .header-icon.bg-blue {
        background: #dbeafe;
        }

        .header-icon.bg-purple {
        background: #f3e8ff;
        }

        .header-icon.bg-blue svg {
        width: 1.25rem;
        height: 1.25rem;
        color: #2563eb;
        }

        .header-icon.bg-purple svg {
        width: 1.25rem;
        height: 1.25rem;
        color: #9333ea;
        }

        .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.25rem;
        }

        .card-description {
        font-size: 0.875rem;
        color: #64748b;
        }

        .card-content {
        padding: 1.5rem;
        }

        /* Scoring Table */
        .scoring-table {
        width: 100%;
        border-collapse: collapse;
        }

        .scoring-table thead tr {
        border-bottom: 2px solid #e2e8f0;
        }

        .scoring-table th {
        text-align: left;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        }

        .scoring-table th.text-right {
        text-align: right;
        }

        .scoring-table tbody tr {
        border-bottom: 1px solid #f1f5f9;
        transition: background-color 0.2s;
        }

        .scoring-table tbody tr:hover {
        background-color: #f8fafc;
        }

        .scoring-table td {
        padding: 1rem;
        }

        .scoring-table td.text-right {
        text-align: right;
        }

        .scoring-number {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.5rem;
        background: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748b;
        font-weight: 500;
        }

        .scoring-factor {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        }

        .scoring-factor svg {
        width: 1rem;
        height: 1rem;
        }

        .scoring-factor .positive {
        color: #16a34a;
        }

        .scoring-factor .negative {
        color: #dc2626;
        }

        .scoring-factor .neutral {
        color: #9ca3af;
        }

        .scoring-factor span {
        color: #0f172a;
        }

        .scoring-bar {
        height: 0.375rem;
        background: #f1f5f9;
        border-radius: 9999px;
        overflow: hidden;
        max-width: 28rem;
        }

        .scoring-bar-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.5s ease;
        }

        .scoring-bar-fill.positive {
        background: linear-gradient(90deg, #4ade80 0%, #16a34a 100%);
        }

        .scoring-bar-fill.negative {
        background: linear-gradient(90deg, #f87171 0%, #dc2626 100%);
        margin-left: auto;
        }

        .scoring-bar-fill.neutral {
        background: #9ca3af;
        }

        .scoring-badge {
        display: inline-block;
        padding: 0.375rem 1rem;
        border: 1px solid;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        min-width: 70px;
        text-align: center;
        }

        .scoring-badge.positive {
        background: #f0fdf4;
        color: #15803d;
        border-color: #bbf7d0;
        }

        .scoring-badge.negative {
        background: #fef2f2;
        color: #b91c1c;
        border-color: #fecaca;
        }

        .scoring-badge.neutral {
        background: #f9fafb;
        color: #374151;
        border-color: #e5e7eb;
        }

        /* Methodology Grid */
        .methodology-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.25rem;
        }

        .methodology-card {
        padding: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 0.75rem;
        transition: all 0.2s;
        }

        .methodology-card:hover {
        border-color: #93c5fd;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .methodology-icon {
        width: 3rem;
        height: 3rem;
        background: #dbeafe;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        transition: background 0.2s;
        }

        .methodology-card:hover .methodology-icon {
        background: #bfdbfe;
        }

        .methodology-icon svg {
        width: 1.5rem;
        height: 1.5rem;
        color: #2563eb;
        }

        .methodology-card h4 {
        font-size: 1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
        }

        .methodology-card p {
        font-size: 0.875rem;
        color: #64748b;
        line-height: 1.5;
        }

        /* Responsive */
        @media (max-width: 768px) {
        .app {
            padding: 1rem;
        }

        .header {
            flex-direction: column;
            gap: 1rem;
        }

        .title {
            font-size: 1.875rem;
        }

        .verdict-content {
            flex-direction: column;
            text-align: center;
        }

        .verdict-header {
            flex-direction: column;
            gap: 0.5rem;
        }

        .verdict-title {
            font-size: 2rem;
        }

        .methodology-grid {
            grid-template-columns: 1fr;
        }

        .scoring-item-left {
            flex-direction: column;
            align-items: flex-start;
        }

        .scoring-bar {
            max-width: 100%;
        }
        }
"""

styles = f"""
    <style>
    {remove_header_footer}
    {page_setup}
    {navbar_styles}
    {cart_button_styles}
    {page_style}
    </style>
"""

def verdict_page():
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
                            on_click = to_overview_page
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
    verdict = st.session_state["final_verdict"]["verdict"]
    confidence = st.session_state["final_verdict"]["confidence"]

    if verdict == "BUY":
        card_color = "buy" 
        card_text = "BUY"  
    elif verdict == "AVOID":
        card_color = "avoid"
        card_text = "AVOID"
    else:
        card_color = "hold"
        card_text = "HOLD"
    with st.container(key = "container"):
        st.markdown(
            f"""
            <div class="verdict-card {card_color}" id="verdictCard">
                    <div class="verdict-content">
                        <div class="verdict-icon {card_color}" id="verdictIcon">
                            <i data-lucide="alert-circle"></i>
                        </div>
                        <div class="verdict-details">
                            <div class="verdict-header">
                                <h2 class="verdict-title {card_color}" id="verdictTitle">{card_text}</h2>
                                <span class="verdict-badge" id="verdictBadge">Confidence: {confidence}%</span>
                            </div>
                            <p class="verdict-description">
                                Based on comprehensive multi-factor analysis
                            </p>
                            <div class="confidence-section">
                                <div class="confidence-label">
                                    <span>Confidence Level</span>
                                    <span id="confidenceValue">{confidence}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill {card_color}" id="progressFill" style = "width:{confidence}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        data = {
            "#": [0, 1, 2, 3],
            "Factor": [
                "Regression Future Growth (1M, Polynomial)",
                "Classification Trend (Bullish/Bearish/Neutral)",
                "Historical ROI (6 months)",
                "Combined Raw Score"
            ],
            "Progress": [
                "Negative",
                "Positive",
                "Negative",
                "Slight Negative"
            ],
            "Score": [-1.0, 1.0, -1.0, -0.3]
        }

        score_df = pd.DataFrame(data)
        table = []
        for index, row in score_df.iterrows():
            name = row["Factor"]
            progress = row["Progress"]
            score = (row["Score"])
            score_type = get_score_type(score)
            table_row = f'<tr><td><div class="scoring-number">{index+1}</div></td><td><div class="scoring-factor"><span>{name}</span></div></td><td><div class="scoring-bar"><div class="scoring-bar-fill {score_type}" style="width: {abs(score)*100}%"></div></div></td><td class="text-right"><span class="scoring-badge {score_type}">{score}</span></td></tr>'
            table.append(table_row)

        st.markdown(
            f"""
                <div class="card">
                    <div class="card-header">
                        <div class="header-icon-wrapper">
                            <div class="header-icon bg-blue">
                                <i data-lucide="trending-up"></i>
                            </div>
                            <div>
                                <h3 class="card-title">Scoring Breakdown</h3>
                                <p class="card-description">Individual factor contributions to final verdict</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-content">
                        <table class="scoring-table" id="scoringTable">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Factor</th>
                                    <th>Progress</th>
                                    <th class="text-right">Score</th>
                                </tr>
                            </thead>
                            <tbody id="scoringTableBody">
                                {"".join(table)}
                            </tbody>
                        </table>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
                <div class="card">
                    <div class="card-header">
                        <div class="header-icon-wrapper">
                            <div class="header-icon bg-purple">
                                <i data-lucide="info"></i>
                            </div>
                            <div>
                                <h3 class="card-title">Methodology</h3>
                                <p class="card-description">Understanding the AI analysis framework</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-content">
                        <div class="methodology-grid" id="methodologyGrid">
                            <!-- Populated by JavaScript -->
                            <div class="methodology-card">
                                <div class="methodology-icon">
                                    <i data-lucide="line-chart"></i>
                                </div>
                                <h4>Regression</h4>
                                <p>Uses Simple, Multiple, and Polynomial Linear Regression to estimate future price levels.</p>
                            </div>
                            <div class="methodology-card">
                                <div class="methodology-icon">
                                    <i data-lucide="brain"></i>
                                </div>
                                <h4>Classification</h4>
                                <p>KNN, Naive Bayes, Decision Tree, SVM, and Logistic Regression classify the market trend.</p>
                            </div>
                            <div class="methodology-card">
                                <div class="methodology-icon">
                                    <i data-lucide="wallet"></i>
                                </div>
                                <h4>$Investment ROI</h4>
                                <p>Simulates a 6-month historical investment to understand medium-term performance.</p>
                            </div>
                            <!--end-->
                        </div>
                    </div>
                </div>
            """,unsafe_allow_html=True
        )