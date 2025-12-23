import streamlit as st
import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from session_state.session_manager import to_classification_page,to_ml_page,to_growth_page,to_verdict_page,to_investment_page,to_overview_page
from datahandeling_and_other.helper import rank_classification_models,build_classification_radar_option,build_best_model_confusion_matrix_option
import pandas as pd
from streamlit_echarts import st_echarts
models = ["KNN", "Naive Bayes", "Decision Tree", "SVM"]

accuracy = [0.2639, 0.3472, 0.3611, 0.3472]
precision = [0.2934, 0.3666, 0.6349, 0.1206]
recall = [0.2639, 0.3472, 0.3611, 0.3472]
f1 = [0.2744, 0.2935, 0.2526, 0.179]
auc = [0.4144, 0.544, 0.5063, 0.539]

# ------------------ Radar Series ------------------
series_data = [
    {
        "name": "KNN",
        "value": [accuracy[0], precision[0], recall[0], f1[0], auc[0]]
    },
    {
        "name": "Naive Bayes",
        "value": [accuracy[1], precision[1], recall[1], f1[1], auc[1]]
    },
    {
        "name": "Decision Tree",
        "value": [accuracy[2], precision[2], recall[2], f1[2], auc[2]]
    },
    {
        "name": "SVM",
        "value": [accuracy[3], precision[3], recall[3], f1[3], auc[3]]
    }
]

# ------------------ ECharts Option ------------------
option = {
    "title": {
        "text": "Classification Models Comparison (Radar)",
        "left": "center"
    },
    "tooltip": {},
    "legend": {
        "bottom": 0
    },
    "radar": {
        "radius": "65%",
        "indicator": [
            {"name": "Accuracy", "max": 1},
            {"name": "Precision", "max": 1},
            {"name": "Recall", "max": 1},
            {"name": "F1 Score", "max": 1},
            {"name": "AUC", "max": 1}
        ]
    },
    "series": [
        {
            "type": "radar",
            "data": series_data,
            "areaStyle": {"opacity": 0.18},
            "lineStyle": {"width": 2},
            "symbolSize": 6
        }
    ]
}

conf_matrix = [
    [120, 35],
    [42, 98]
]

labels = ["Class 0", "Class 1"]

# Convert matrix to ECharts format
data = []
for i in range(len(conf_matrix)):
    for j in range(len(conf_matrix[0])):
        data.append([j, i, conf_matrix[i][j]])

# ------------------ ECharts Option ------------------
option1 = {
    "tooltip": {
        "position": "top"
    },
    "grid": {
        "height": "60%",
        "top": "10%"
    },
    "xAxis": {
        "type": "category",
        "data": labels,
        "name": "Predicted Label",
        "splitArea": {"show": True}
    },
    "yAxis": {
        "type": "category",
        "data": labels,
        "name": "Actual Label",
        "splitArea": {"show": True}
    },
    "visualMap": {
        "min": 0,
        "max": max(max(row) for row in conf_matrix),
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": "5%"
    },
    "series": [
        {
            "name": "Confusion Matrix",
            "type": "heatmap",
            "data": data,
            "label": {
                "show": True
            },
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }
    ]
}
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
.st-key-nav-btn-3 .stButton button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--primary-dark)
    );
    color: #ffffff;
    border: none;
}

.st-key-nav-btn-3 .stButton button:hover {
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

kpi_card_1_style = """
.st-key-kpi-card-1 {
    grid-column: span 2;
    grid-row: span 2;
}
.st-key-kpi-card-1 .kpi-header {
    display: flex;
    flex-direction: column;     /* COLUMN layout */
    align-items: flex-start;    /* left aligned */
    gap: 0.4rem;
}
.st-key-kpi-card-1 .card-description {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.4;
}
.st-key-kpi-card-1::before {
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

kpi_card_1_style_positive = """
.st-key-kpi-card-1 {
    border-left:4px solid #16a34a;
}
.st-key-kpi-card-1:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(22, 163, 74, 0.25);
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

        .card-content.less-padding {
            padding: 1.2rem;
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

        .badge.neutral {
            background: #64748b;
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
    {kpi_card_1_style}
    {kpi_card_1_style_positive}
    {card_styles}
    {chart_styles}
    </style>
"""

def classification_page():
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

    rows = []
    for name in ["KNN", "Naive Bayes", "Decision Tree", "SVM"]:
                res = st.session_state["classification_results"]["models"][name]
                rows.append(
                    {
                        "Model": name,
                        "Accuracy": res["accuracy"],
                        "Precision (weighted)": res["precision"],
                        "Recall (weighted)": res["recall"],
                        "F1 (weighted)": res["f1"],
                        "AUC (OVR)": res["auc"],
                    }
                )
    clf_metrics_df = pd.DataFrame(rows)
    classification_model_ranks = rank_classification_models(clf_metrics_df)
    with st.container(key = "kpi-grid"):
        with st.container(key = "kpi-card-2"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Precision</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 3v16a2 2 0 0 0 2 2h16"></path>
                        <path d="M18 17V9"></path>
                        <path d="M13 17V5"></path>
                        <path d="M8 17v-3"></path>
                    </svg>
                </div>
                <div class="kpi-value">{round(classification_model_ranks.iloc[0]["Precision (weighted)"],2)}</div>
                <div class="kpi-change positive">
                    <span>↗</span> +12.5% vs avg volume
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-1"):
            st.markdown(f"""
                <div class="card-header">
                        <div class="card-title">Best Classification Model</div>
                        <div class="card-description">Model Ranking</div>
                    </div>
                    <div class="card-content less-padding">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                            <span class="badge success">{classification_model_ranks.iloc[0]["Model"]}</span>
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-bottom: 0.5rem;">
                                    <span style="color: #64748b;">Accuracy</span>
                                    <span style="color: #16a34a; font-weight: 600;">{round(classification_model_ranks.iloc[0]["Accuracy"]*100,2)}%</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill green" style="width: {int(classification_model_ranks.iloc[0]["Accuracy"]*100)}%;"></div>
                                </div>
                            </div>
                        </div>
                        <div class="verdict-list">
                            <p>• High volatility detected in short-term patterns</p>
                            <p>• Mixed signals from technical indicators</p>
                            <p>• High volatility detected in short-term patterns</p>
                    </div>
            """,unsafe_allow_html=True)
        
        with st.container(key = "kpi-card-3"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">Recall</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 7h6v6"></path>
                        <path d="m22 7-8.5 8.5-5-5L2 17"></path>
                    </svg>
                </div>
                <div class="kpi-value">{round(classification_model_ranks.iloc[0]["Recall (weighted)"],2)}</div>
                <div class="kpi-change negative">
                    <span>↗</span> +12.5% vs avg volume
                </div>
            """,unsafe_allow_html=True)
        
        
        with st.container(key = "kpi-card-4"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">F1</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path>
                    </svg>
                </div>
                <div class="kpi-value">{round(classification_model_ranks.iloc[0]["F1 (weighted)"],2)}</div>
                <div class="kpi-change neutral">
                    <span>→</span> 1.89% range
                </div>
            """,unsafe_allow_html=True)

        with st.container(key = "kpi-card-5"):
            st.markdown(f"""
                <div class="kpi-header">
                    <span class="kpi-title">AUC</span>
                    <svg class="kpi-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                        <line x1="9" y1="9" x2="9.01" y2="9"></line>
                        <line x1="15" y1="9" x2="15.01" y2="9"></line>
                    </svg>
                </div>
                <div class="kpi-value">{round(classification_model_ranks.iloc[0]["AUC (OVR)"],2)}</div>
                <div class="kpi-change positive">
                    <span>↗</span> Above EMA
                </div>
            """,unsafe_allow_html=True)
        
        

    with st.container(key = "chart-grid"):
        with st.container(key = "card-1"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Model Performance Comparison</div>
                    <div class="card-description">Radar Chart</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-1"):
                with st.container(key = "chart-container-1"):
                    st_echarts(build_classification_radar_option(clf_metrics_df))
        with st.container(key = "card-2"):
            st.markdown(
                """
                <div class="card-header">
                    <div class="card-title">Confusion Matrix</div>
                    <div class="card-description">Best Model</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "card-content-2"):
                with st.container(key = "chart-container-2"):
                    st_echarts(build_best_model_confusion_matrix_option(classification_model_ranks,st.session_state["classification_results"]))

    # with st.container(key = "card-3"):
    #     st.markdown(
    #         """
    #         <div class="card-header">
    #             <div class="card-title">Market Trend Analysis (30d)</div>
    #             <div class="card-description">Price movement with moving averages and volume overlay</div>
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )
    #     with st.container(key = "card-content-3"):
    #         with st.container(key = "chart-container-large"):
    #             st_echarts(option2)
    #             # pass




