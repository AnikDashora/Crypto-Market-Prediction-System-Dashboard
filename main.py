import streamlit as st
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from session_state.session_manager import initialize_session_states
from view.landing_page import landingpage
from view.overview import overview_page
from view.ml_prediction import ml_page
from view.classification import classification_page
from view.investment_simulator import investment_page
from view.verdict import verdict_page
from view.growth_comparison import growth_page

initialize_session_states()

if(st.session_state["pages"] == 0):
    landingpage()
elif(st.session_state["pages"] == 1):
    overview_page()
elif(st.session_state["pages"] == 2):
    ml_page()
elif(st.session_state["pages"] == 3):
    classification_page()
elif(st.session_state["pages"] == 4):
    investment_page()
elif(st.session_state["pages"] == 5):
    growth_page()
elif(st.session_state["pages"] == 6):
    verdict_page()

if(__name__ == "__main__"):
    pass