import streamlit as st

PAGES = (
    "Crypto Market Prediction System/view/landing_page",#0
    "Crypto Market Prediction System/view/overview_page",#1
    "Crypto Market Prediction System/view/ml_page",#2
    "Crypto Market Prediction System/view/classification_page",#3
    "Crypto Market Prediction System/view/investment_page",#4
    "Crypto Market Prediction System/view/growth_page",#5
    "Crypto Market Prediction System/view/verdict_page",#6
)

def initialize_session_states():
    if("pages" not in st.session_state):
        st.session_state["pages"] = 0
    if("coin_id" not in st.session_state):
        st.session_state["coin_id"] = None
    if("investment_amount" not in st.session_state):
        st.session_state["investment_amount"] = None
    if("coin_overview" not in st.session_state):
        st.session_state["coin_overview"] = None
    if("market_data" not in st.session_state):
        st.session_state["market_data"] = None
    if("current_price" not in st.session_state):
        st.session_state["current_price"] = None
    if("price_change_24h" not in st.session_state):
        st.session_state["price_change_24h"] = None
    if("market_cap" not in st.session_state):
        st.session_state["market_cap"] = None
    if("total_volume" not in st.session_state):
        st.session_state["total_volume"] = None
    
    if("market_chart" not in st.session_state):
        st.session_state["market_chart"] = None

    if("df_daily" not in st.session_state):
        st.session_state["df_daily"] = None
    if("df_daily_ml" not in st.session_state):
        st.session_state["df_daily_ml"] = None

    if("regression_results" not in st.session_state):
        st.session_state["regression_results"] = None
    
    if("classification_results" not in st.session_state):
        st.session_state["classification_results"] = None

    if("future_predictions" not in st.session_state):
        st.session_state["future_predictions"] = None
    if("trend_majority" not in st.session_state):
        st.session_state["trend_majority"] = None

    if("investment_result" not in st.session_state):
        st.session_state["investment_result"] = None
    if("top_growth_df" not in st.session_state):
        st.session_state["top_growth_df"] = None

    if("investment_result" not in st.session_state):
        st.session_state["investment_result"] = None
    if("top_growth_df" not in st.session_state):
        st.session_state["top_growth_df"] = None

    if("comparative_history" not in st.session_state):
        st.session_state["comparative_history"] = None
    if("final_verdict" not in st.session_state):
        st.session_state["final_verdict"] = None
        

def to_overview_page():
    st.session_state["pages"] = 1

def to_ml_page():
    st.session_state["pages"] = 2

def to_classification_page():
    st.session_state["pages"] = 3

def to_investment_page():
    st.session_state["pages"] = 4

def to_growth_page():
    st.session_state["pages"] = 5

def to_verdict_page():
    st.session_state["pages"] = 6


