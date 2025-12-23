import streamlit as st
import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
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
.st-key-nav-btn-5 .stButton button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-5 .stButton button:hover {
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


styles = f"""
    <style>
    {remove_header_footer}
    {page_setup}
    {navbar_styles}
    {cart_button_styles}
    </style>
"""

def growth_page():
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
                    overview_col,ml_col,classification_col,investment_col,growth_col,verdict_col = st.columns(6)
                    
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
                    with growth_col:
                        st.button(
                            label="Growth Comparison",
                            key = "nav-btn-5",
                            type="secondary",
                            on_click=to_growth_page
                        )
                    with verdict_col:
                        st.button(
                            label="AI Verdict",
                            key = "nav-btn-6",
                            type="secondary",
                            on_click=to_verdict_page
                        )

