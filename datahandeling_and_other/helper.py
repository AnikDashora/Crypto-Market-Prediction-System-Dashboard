import math
import time
import datetime as dt
from typing import Dict, Any, List, Optional,Tuple
from datetime import timedelta
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder, label_binarize
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# GLOBAL CONSTANTS & SETTINGS

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
VS_CURRENCY = "usd"

TIMELINE_TO_DAYS = {
    "1 Hour": 1,        
    "1 Day": 1,
    "1 Week": 7,
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
}

TIMELINE_TO_DAY_OFFSET = {
    "1 Hour": 1.0 / 24.0,
    "1 Day": 1.0,
    "1 Week": 7.0,
    "1 Month": 30.0,
    "3 Months": 90.0,
    "6 Months": 180.0,
    "1 Year": 365.0,
}

POSITIVE_WORDS = {
    "bull", "bullish", "surge", "rally", "gain", "gains", "up", "positive", "buy",
    "strong", "boom", "soar", "soaring", "pump", "green", "record", "breakout",
    "optimistic", "support", "growth", "recover", "recovery"
}

NEGATIVE_WORDS = {
    "bear", "bearish", "crash", "dump", "down", "drop", "loss", "losses",
    "negative", "sell", "panic", "fear", "red", "collapse", "plunge",
    "weak", "uncertain", "ban", "lawsuit", "hack", "fraud"
}

# UTILITY FUNCTIONS

def safe_get(url: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    """Simple GET wrapper with retries for JSON response."""
    for _ in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            time.sleep(1)
    return None


def fetch_coin_overview(coin_id: str) -> Optional[Dict[str, Any]]:
    """Fetch basic coin overview from CoinGecko."""
    url = f"{COINGECKO_API_BASE}/coins/{coin_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false",
    }
    return safe_get(url, params=params)


def fetch_historical_market_chart(coin_id: str, days: str = "max") -> Optional[Dict[str, Any]]:
    """Fetch historical market chart (prices, market_caps, total_volumes)."""
    url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": VS_CURRENCY,
        "days": days,
    }
    return safe_get(url, params=params)


def build_daily_price_dataframe(market_chart: Dict[str, Any]) -> pd.DataFrame:
    """
    Builds daily close dataframe and computes:
    - EMA(10)
    - SMA(9) of EMA(10)
    - RSI(14)
    - MACD (12,26,9)
    All calculated indicators have NaN filled with column mean.
    """
    prices = market_chart.get("prices", [])
    total_vol = market_chart.get("total_volumes", [])
    market_cap = market_chart.get("market_caps", [])

    if not (prices and total_vol and market_cap):
        return pd.DataFrame()

    # Create DataFrames
    price_df = pd.DataFrame(prices, columns=["timestamp", "price"])
    volume_df = pd.DataFrame(total_vol, columns=["timestamp", "total_volume"])
    market_cap_df = pd.DataFrame(market_cap, columns=["timestamp", "market_cap"])

    # Merge on timestamp
    df = price_df.merge(volume_df, on="timestamp", how="inner")
    df = df.merge(market_cap_df, on="timestamp", how="inner")

    # Convert timestamp
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Set index
    df = df.set_index("date")[["price", "total_volume", "market_cap"]]

    # Daily close
    daily = df.resample("1D").last().dropna()

    # ===================== FORMATTED COLUMNS =====================
    daily["market_cap_fmt"] = daily["market_cap"].apply(format_volume)
    daily["price_fmt"] = daily["price"].apply(format_volume)
    daily["total_volume_fmt"] = daily["total_volume"].apply(format_volume)

    # ===================== EMA & SMA =====================
    daily["ema_10"] = daily["price"].ewm(span=10, adjust=False).mean()
    daily["sma_9_ema"] = daily["ema_10"].rolling(9).mean()

    # ===================== RSI (14) =====================
    delta = daily["price"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()

    rs = avg_gain / avg_loss
    daily["rsi_14"] = 100 - (100 / (1 + rs))

    # ===================== MACD =====================
    ema_12 = daily["price"].ewm(span=12, adjust=False).mean()
    ema_26 = daily["price"].ewm(span=26, adjust=False).mean()

    daily["macd"] = ema_12 - ema_26
    daily["macd_signal"] = daily["macd"].ewm(span=9, adjust=False).mean()
    daily["macd_hist"] = daily["macd"] - daily["macd_signal"]

    # ===================== FILL NaN WITH COLUMN MEAN =====================
    indicator_cols = [
        "ema_10",
        "sma_9_ema",
        "rsi_14",
        "macd",
        "macd_signal",
        "macd_hist",
    ]

    for col in indicator_cols:
        mean_val = daily[col].mean(skipna=True)
        daily[col] = daily[col].fillna(mean_val)

    daily.reset_index(inplace=True)
    daily.sort_values("date")
    return daily



def add_features_and_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add predictive features and classification labels.
    Features:
        - time_idx
        - return_1d
        - rolling_mean_7
        - rolling_std_7
    Label:
        - trend_label (Bullish / Bearish / Neutral) based on 3-day future return.
    """
    df = df.copy()
    df["time_idx"] = np.arange(len(df))
    df["return_1d"] = df["price"].pct_change()
    df["rolling_mean_7"] = df["price"].rolling(window=7).mean()
    df["rolling_std_7"] = df["price"].rolling(window=7).std()

    df["future_return_3d"] = df["price"].pct_change(periods=3).shift(-3)
    conditions = [
        df["future_return_3d"] > 0.01,
        df["future_return_3d"] < -0.01,
    ]
    choices = ["Bullish", "Bearish"]
    df["trend_label"] = np.select(conditions, choices, default="Neutral")

    df = df.dropna(subset=["return_1d", "rolling_mean_7", "rolling_std_7", "future_return_3d"])
    return df


# REGRESSION MODELS (UNIT II)

def train_regression_models(df_ml: pd.DataFrame) -> Dict[str, Any]:
    """
    Train Simple Linear, Multiple Linear, Polynomial Regression models.
    Returns models and evaluation metrics.
    """
    results: Dict[str, Any] = {}

    X_time = df_ml[["time_idx"]].values
    y = df_ml["price"].values

    X_multi = df_ml[["time_idx", "return_1d", "rolling_mean_7", "rolling_std_7"]].fillna(0.0).values

    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X_time)

    X_train_time, X_test_time, y_train, y_test, train_idx, test_idx = train_test_split(
        X_time, y, df_ml.index.values, test_size=0.2, shuffle=False
    )

    X_train_multi = X_multi[np.isin(df_ml.index.values, train_idx)]
    X_test_multi = X_multi[np.isin(df_ml.index.values, test_idx)]

    X_train_poly = poly.transform(X_train_time)
    X_test_poly = poly.transform(X_test_time)

    simple_model = LinearRegression()
    simple_model.fit(X_train_time, y_train)
    y_pred_simple = simple_model.predict(X_test_time)

    multi_model = LinearRegression()
    multi_model.fit(X_train_multi, y_train)
    y_pred_multi = multi_model.predict(X_test_multi)

    poly_model = LinearRegression()
    poly_model.fit(X_train_poly, y_train)
    y_pred_poly = poly_model.predict(X_test_poly)

    def regression_metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = math.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        return {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2,
        }

    results["simple"] = {
        "model": simple_model,
        "metrics": regression_metrics(y_test, y_pred_simple),
        "y_test": y_test,
        "y_pred": y_pred_simple,
    }
    results["multiple"] = {
        "model": multi_model,
        "metrics": regression_metrics(y_test, y_pred_multi),
        "y_test": y_test,
        "y_pred": y_pred_multi,
    }
    results["polynomial"] = {
        "model": poly_model,
        "metrics": regression_metrics(y_test, y_pred_poly),
        "y_test": y_test,
        "y_pred": y_pred_poly,
    }
    results["poly_transformer"] = poly
    results["train_idx"] = train_idx
    results["test_idx"] = test_idx

    return results


def predict_future_prices(
    df_ml: pd.DataFrame,
    reg_results: Dict[str, Any],
    timeline_offsets: Dict[str, float],
) -> Dict[str, Dict[str, float]]:
    """
    Predict future prices for each timeline using all three regression models.
    Uses last known feature values and extrapolates time index.
    """
    future_predictions: Dict[str, Dict[str, float]] = {}
    last_row = df_ml.iloc[-1]
    last_time_idx = float(last_row["time_idx"])
    last_return = float(last_row["return_1d"])
    last_mean = float(last_row["rolling_mean_7"])
    last_std = float(last_row["rolling_std_7"])

    simple_model = reg_results["simple"]["model"]
    multi_model = reg_results["multiple"]["model"]
    poly_model = reg_results["polynomial"]["model"]
    poly_trans = reg_results["poly_transformer"]

    for label, offset_days in timeline_offsets.items():
        future_idx = last_time_idx + offset_days
        X_simple = np.array([[future_idx]])
        X_multi = np.array([[future_idx, last_return, last_mean, last_std]])
        X_poly = poly_trans.transform(X_simple)

        p_simple = float(simple_model.predict(X_simple)[0])
        p_multi = float(multi_model.predict(X_multi)[0])
        p_poly = float(poly_model.predict(X_poly)[0])

        future_predictions[label] = {
            "Simple Linear": p_simple,
            "Multiple Linear": p_multi,
            "Polynomial": p_poly,
        }

    return future_predictions


# CLASSIFICATION MODELS (UNIT III)

def train_classification_models(df_ml: pd.DataFrame) -> Dict[str, Any]:
    """
    Train KNN, Naive Bayes, Decision Tree, SVM (and Logistic Regression for syllabus) on trend_label.
    Returns models and performance metrics.
    """
    feature_cols = ["time_idx", "return_1d", "rolling_mean_7", "rolling_std_7"]
    X = df_ml[feature_cols].fillna(0.0).values
    y_raw = df_ml["trend_label"].values

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    models: Dict[str, Any] = {
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "SVM": SVC(kernel="rbf", probability=True, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, multi_class="auto"),
    }

    results: Dict[str, Any] = {}

    classes = np.unique(y)
    y_test_binarized = label_binarize(y_test, classes=classes)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)
        else:
            y_proba = None

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        cm = confusion_matrix(y_test, y_pred)

        if y_proba is not None and len(np.unique(y_test)) > 1:
            try:
                auc = roc_auc_score(y_test_binarized, y_proba, multi_class="ovr")
            except Exception:
                auc = np.nan
        else:
            auc = np.nan

        results[name] = {
            "model": model,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "auc": auc,
            "confusion_matrix": cm,
            "y_test": y_test,
            "y_pred": y_pred,
        }

    return {
        "models": results,
        "label_encoder": label_encoder,
        "X_test": X_test,
        "y_test": y_test,
        "classes": classes,
    }


def majority_trend_from_models(
    clf_results: Dict[str, Any],
    latest_features: np.ndarray,
) -> Tuple[str, float]:
    """
    Returns:
    - Majority trend label
    - Confidence percentage based on model agreement
    """
    label_encoder: LabelEncoder = clf_results["label_encoder"]
    models = clf_results["models"]

    predictions = []

    for _, res in models.items():
        model = res["model"]
        pred = model.predict(latest_features.reshape(1, -1))[0]
        predictions.append(pred)

    if not predictions:
        return "Neutral", 0.0

    values, counts = np.unique(predictions, return_counts=True)
    majority_class = values[np.argmax(counts)]
    majority_label = label_encoder.inverse_transform([majority_class])[0]

    confidence = (counts.max() / len(predictions)) * 100

    return str(majority_label), round(confidence, 2)

# INVESTMENT RETURN SIMULATOR

def compute_investment_return(
    df_daily: pd.DataFrame,
    investment_amount: float,
    months_ago: int = 6,
) -> Dict[str, Any]:
    """
    Simulate investing a fixed amount months_ago and holding until latest close.
    Returns ROI metrics.
    """
    result = {
        "possible": False,
        "investment_amount": investment_amount,
        "coins_bought": None,
        "past_price": None,
        "current_price": None,
        "current_value": None,
        "profit_loss": None,
        "roi_percent": None,
        "verdict": None,
    }

    if df_daily.empty or investment_amount <= 0:
        return result

    df = df_daily.copy()
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    latest_date = df.index.max()
    target_date = latest_date - pd.Timedelta(days=int(months_ago * 30))

    df_before = df[df.index <= target_date]
    if df_before.empty:
        past_price = float(df["price"].iloc[0])
    else:
        past_price = float(df_before["price"].iloc[-1])

    current_price = float(df["price"].iloc[-1])

    if past_price <= 0:
        return result

    coins_bought = investment_amount / past_price
    current_value = coins_bought * current_price
    profit_loss = current_value - investment_amount
    roi_percent = (profit_loss / investment_amount) * 100.0

    if roi_percent > 5:
        verdict = "Good Profit"
    elif roi_percent < -5:
        verdict = "Loss"
    else:
        verdict = "Flat / Slight Move"

    result.update(
        {
            "possible": True,
            "coins_bought": coins_bought,
            "past_price": past_price,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "roi_percent": roi_percent,
            "verdict": verdict,
        }
    )
    return result

# TOP GROWTH COMPARISON

def fetch_top_growth_coins(
    vs_currency: str = "usd",
    days: int = 30,
    exclude_coin_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch top 5 fastest growing coins (by 30d price change %) from CoinGecko.
    """
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "30d",
    }
    data = safe_get(url, params=params)
    if data is None:
        return pd.DataFrame(columns=["id", "symbol", "name", "growth_30d"])

    rows = []
    for item in data:
        coin_id = item.get("id")
        if exclude_coin_id and coin_id == exclude_coin_id:
            continue
        growth = item.get("price_change_percentage_30d_in_currency")
        if growth is None:
            growth = item.get("price_change_percentage_30d")
        if growth is not None:
            rows.append(
                {
                    "id": coin_id,
                    "symbol": item.get("symbol"),
                    "name": item.get("name"),
                    "growth_30d": float(growth),
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.sort_values("growth_30d", ascending=False).head(5)
    return df


def fetch_30d_history_for_coins(coin_ids: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Fetch last 30 days of daily prices for given coin IDs.
    """
    history: Dict[str, pd.DataFrame] = {}
    for cid in coin_ids:
        data = fetch_historical_market_chart(cid, days="30")
        if data is None:
            continue
        df = build_daily_price_dataframe(data)
        if df.empty:
            continue
        history[cid] = df
    return history

# NEWS & SENTIMENT

def fetch_news_from_newsapi(
    query: str,
    api_key: str,
    page_size: int = 20,
) -> List[Dict[str, Any]]:
    """
    Fetch crypto news for given query using NewsAPI.
    Requires a valid API key.
    """
    if not api_key:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": api_key,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get("articles", [])
    except Exception:
        return []


def sentiment_score_for_text(text: str) -> float:
    """
    Very simple lexicon-based sentiment score.
    Returns score in [-1, 1].
    """
    if not text:
        return 0.0
    text = text.lower()
    tokens = []
    current_token = []
    for ch in text:
        if ch.isalpha():
            current_token.append(ch)
        else:
            if current_token:
                tokens.append("".join(current_token))
                current_token = []
    if current_token:
        tokens.append("".join(current_token))

    if not tokens:
        return 0.0

    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    score = (pos - neg) / float(len(tokens))
    score = max(min(score, 1.0), -1.0)
    return score


def analyze_news_sentiment(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate sentiment for a list of NewsAPI articles.
    """
    scores = []
    detailed = []
    for art in articles:
        title = art.get("title") or ""
        desc = art.get("description") or ""
        content = title + " " + desc
        score = sentiment_score_for_text(content)
        scores.append(score)
        detailed.append(
            {
                "title": title,
                "description": desc,
                "url": art.get("url"),
                "published_at": art.get("publishedAt"),
                "sentiment_score": score,
            }
        )

    if not scores:
        return {
            "mean_score": 0.0,
            "sentiment_label": "Neutral",
            "details": [],
        }

    mean_score = float(np.mean(scores))
    if mean_score > 0.02:
        label = "Bullish"
    elif mean_score < -0.02:
        label = "Bearish"
    else:
        label = "Neutral"

    return {
        "mean_score": mean_score,
        "sentiment_label": label,
        "details": detailed,
    }

# FINAL AI VERDICT ENGINE

def compute_final_verdict(
    current_price: float,
    future_predictions: Dict[str, Dict[str, float]],
    classification_trend: str,
    news_sentiment_label: str,
    investment_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Combine regression trend, classification output, news sentiment, and ROI into a Buy/Hold/Avoid decision.
    """
    future_growth_norm = 0.0
    if "1 Month" in future_predictions:
        pred_poly = future_predictions["1 Month"].get("Polynomial")
        if pred_poly and current_price > 0:
            growth = (pred_poly - current_price) / current_price
            future_growth_norm = max(min(growth * 2.0, 1.0), -1.0)

    if classification_trend == "Bullish":
        class_score = 1.0
    elif classification_trend == "Bearish":
        class_score = -1.0
    else:
        class_score = 0.0

    if news_sentiment_label == "Bullish":
        news_score = 1.0
    elif news_sentiment_label == "Bearish":
        news_score = -1.0
    else:
        news_score = 0.0

    roi_score = 0.0
    if investment_result.get("possible"):
        roi_pct = float(investment_result.get("roi_percent") or 0.0)
        if roi_pct > 0:
            roi_score = 1.0
        elif roi_pct < 0:
            roi_score = -1.0
        else:
            roi_score = 0.0

    combined_raw = (
        0.4 * future_growth_norm
        + 0.25 * class_score
        + 0.2 * news_score
        + 0.15 * roi_score
    )
    combined_raw = max(min(combined_raw, 1.0), -1.0)

    if combined_raw > 0.4:
        verdict = "BUY"
    elif combined_raw < -0.2:
        verdict = "AVOID"
    else:
        verdict = "HOLD"

    confidence = int(abs(combined_raw) * 100)

    return {
        "verdict": verdict,
        "confidence": confidence,
        "future_growth_norm": future_growth_norm,
        "class_score": class_score,
        "news_score": news_score,
        "roi_score": roi_score,
        "combined_raw": combined_raw,
    }

# STREAMLIT UI UTILITIES

def set_dark_neon_theme():
    """
    Inject basic dark + neon CSS into Streamlit.
    """
    css = """
    <style>
    body {
        background-color: #05060a;
        color: #e0e0e0;
    }
    .stApp {
        background: radial-gradient(circle at top, #141824, #05060a);
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background: #05060a;
    }
    h1, h2, h3, h4 {
        color: #5af0ff;
        text-shadow: 0 0 10px rgba(90, 240, 255, 0.6);
    }
    .css-1cpxqw2, .css-10trblm {
        color: #e0e0e0;
    }
    .neon-box {
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #5af0ff;
        box-shadow: 0 0 20px rgba(90, 240, 255, 0.5);
        background: rgba(10, 10, 25, 0.9);
    }
    .metric-container {
        background: rgba(15, 15, 35, 0.95);
        border-radius: 8px;
        padding: 0.5rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def format_usd(x: Optional[float]) -> str:
    if x is None or np.isnan(x):
        return "-"
    if abs(x) >= 1_000_000_000:
        return f"${x/1_000_000_000:,.2f}B"
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:,.2f}M"
    return f"${x:,.2f}"


def format_volume(value):
    """
    Formats large numeric values into human-readable stock volume format.
    Examples:
    950       -> 950
    1_200     -> 1.2K
    2_500_000 -> 2.5M
    3_600_000_000 -> 3.6B
    1_200_000_000_000 -> 1.2T
    """
    if value is None:
        return "0"

    abs_value = abs(value)

    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif abs_value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)
    

def build_market_cap_line_option(df_daily):
    """
    Builds an ECharts line chart option for last 30 days market cap.
    Returns the option dictionary (does not render).
    """

    if df_daily.empty or "market_cap" not in df_daily.columns:
        return {}

    # Ensure datetime
    df = df_daily.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Filter last 30 days
    last_date = df["date"].max()
    start_date = last_date - timedelta(days=30)
    df_30 = df[df["date"] >= start_date]

    # Prepare data
    dates = df_30["date"].dt.strftime("%Y-%m-%d").tolist()
    market_caps = df_30["market_cap"].tolist()

    option = {
        "tooltip": {
            "trigger": "axis",
            "valueFormatter": "function (value) { return value.toLocaleString(); }"
        },
        "xAxis": {
            "type": "category",
            "data": dates,
            "boundaryGap": False
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "axisLabel": {
                "show": False
            },
            "axisTick": {
                "show": True
            },
            "splitLine": {
                "show": True
            }
        },
        "series": [
            {
                "name": "Market Cap",
                "type": "line",
                "data": market_caps,
                "smooth": True,
                "lineStyle": {
                    "width": 3,
                    "color": "#10b981"
                },
                "itemStyle": {
                    "color": "#10b981"
                },
                "areaStyle": {
                    "opacity": 0.15
                }
            }
        ],
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        }
    }

    return option


def build_volume_bar_option(daily_df):
    """
    Builds an ECharts bar chart option for last 7 days volume.
    - Green bar if volume increased vs previous day
    - Red bar if volume decreased
    - Y-axis labels hidden
    Returns option dict
    """

    if daily_df.empty or "total_volume" not in daily_df.columns:
        return {}

    df = daily_df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Get last 7 days
    last_date = df["date"].max()
    start_date = last_date - timedelta(days=7)
    df_7 = df[df["date"] >= start_date].sort_values("date")

    # X-axis labels (Day names)
    days = df_7["date"].dt.strftime("%a").tolist()
    volumes = df_7["total_volume"].tolist()

    # Color logic
    colors = []
    for i in range(len(volumes)):
        if i == 0:
            colors.append("#16a34a")  # First bar green
        else:
            colors.append(
                "#16a34a" if volumes[i] >= volumes[i - 1] else "#dc2626"
            )

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"}
        },
        "xAxis": {
            "type": "category",
            "data": days
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"show": True},
            "axisTick": {"show": True},
            "splitLine": {"show": True}
        },
        "series": [
            {
                "name": "Volume",
                "type": "bar",
                "data": [
                    {
                        "value": volumes[i],
                        "itemStyle": {"color": colors[i]}
                    }
                    for i in range(len(volumes))
                ],
                "barWidth": "55%",
                "borderRadius": [6, 6, 0, 0]
            }
        ],
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        }
    }

    return option


def build_price_ema_line_option(df_daily):
    """
    Builds an ECharts line chart for:
    - Price
    - EMA(10)
    - SMA(9) of EMA(10)

    Legend on top
    Y-axis labels hidden
    Returns option dict
    """

    required_cols = {"date", "price", "ema_10", "sma_9_ema"}
    if df_daily.empty or not required_cols.issubset(df_daily.columns):
        return {}

    df = df_daily.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Use recent data (optional – keeps chart clean)
    # df = df.tail(60)

    dates = df["date"].dt.strftime("%Y-%m-%d").tolist()
    prices = df["price"].tolist()
    ema_10 = df["ema_10"].tolist()
    sma_9_ema = df["sma_9_ema"].tolist()

    option = {
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "top": "2%",
            "data": ["Price", "EMA 10", "SMA 9 EMA"]
        },
        "xAxis": {
            "type": "category",
            "data": dates,
            "boundaryGap": False
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "axisLabel": {"show": True},
            "axisTick": {"show": True},
            "splitLine": {"show": True}
        },
        "series": [
            {
                "name": "Price",
                "type": "line",
                "data": prices,
                "smooth": True,
                "lineStyle": {
                    "width": 2,
                    "color": "#3b82f6"
                },
                "itemStyle": {
                    "color": "#3b82f6"
                }
            },
            {
                "name": "EMA 10",
                "type": "line",
                "data": ema_10,
                "smooth": True,
                "lineStyle": {
                    "width": 2,
                    "type": "dashed",
                    "color": "#22c55e"
                },
                "itemStyle": {
                    "color": "#22c55e"
                }
            },
            {
                "name": "SMA 9 EMA",
                "type": "line",
                "data": sma_9_ema,
                "smooth": True,
                "lineStyle": {
                    "width": 2,
                    "type": "dotted",
                    "color": "#f59e0b"
                },
                "itemStyle": {
                    "color": "#f59e0b"
                }
            }
        ],
        "grid": {
            "top": "15%",
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        }
    }

    return option


def rank_models(model_metrics):
    """
    Ranks all models from highest to lowest performance
    using normalized composite scoring.

    model_metrics: List of dicts with keys:
    ['Model', 'MAE', 'MSE', 'RMSE', 'R²']

    Returns:
    - Ranked DataFrame (best model on top)
    """

    df = pd.DataFrame(model_metrics)

    # Normalize error metrics (lower is better)
    df["MAE_norm"] = 1 - (df["MAE"] / df["MAE"].max())
    df["MSE_norm"] = 1 - (df["MSE"] / df["MSE"].max())
    df["RMSE_norm"] = 1 - (df["RMSE"] / df["RMSE"].max())

    # Normalize R² (higher is better)
    df["R2_norm"] = df["R²"] / df["R²"].max()

    # Composite score (equal weight)
    df["Final_Score"] = (
        df["MAE_norm"] +
        df["MSE_norm"] +
        df["RMSE_norm"] +
        df["R2_norm"]
    ) / 4

    # Rank models (highest score = best)
    ranked_df = df.sort_values("Final_Score", ascending=False).reset_index(drop=True)

    # Add ranking column
    ranked_df.insert(0, "Rank", ranked_df.index + 1)

    return ranked_df

def build_model_metrics_line_option(df):
    """
    Builds an ECharts line chart option for
    MAE, MSE, RMSE, and R² across models.

    Input df columns required:
    ['Model', 'MAE', 'MSE', 'RMSE', 'R²']

    Returns:
    - option (dict)
    """

    required_cols = {"Model", "MAE", "MSE", "RMSE", "R²"}
    if df.empty or not required_cols.issubset(df.columns):
        return {}

    # Ensure correct order
    df = df.copy().reset_index(drop=True)

    models = df["Model"].astype(str).tolist()

    mae = df["MAE"].apply(lambda x: None if pd.isna(x) else x).tolist()
    mse = df["MSE"].apply(lambda x: None if pd.isna(x) else x).tolist()
    rmse = df["RMSE"].apply(lambda x: None if pd.isna(x) else x).tolist()
    r2 = df["R²"].apply(lambda x: None if pd.isna(x) else x).tolist()

    option = {
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "top": "2%",
            "data": ["MAE", "MSE", "RMSE", "R²"]
        },
        "xAxis": {
            "type": "category",
            "data": models
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "axisLabel": {"show": True},
            "axisTick": {"show": True},
            "splitLine": {"show": True}
        },
        "series": [
            {
                "name": "MAE",
                "type": "line",
                "data": mae,
                "smooth": True,
                "lineStyle": {"width": 2}
            },
            {
                "name": "MSE",
                "type": "line",
                "data": mse,
                "smooth": True,
                "lineStyle": {"width": 2}
            },
            {
                "name": "RMSE",
                "type": "line",
                "data": rmse,
                "smooth": True,
                "lineStyle": {"width": 2}
            },
            {
                "name": "R²",
                "type": "line",
                "data": r2,
                "smooth": True,
                "lineStyle": {"width": 2}
            }
        ],
        "grid": {
            "top": "18%",
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        }
    }

    return option


def build_prediction_multibar_option(df):
    """
    Builds a multi-bar ECharts option comparing
    Simple Linear, Multiple Linear, and Polynomial predictions
    across timelines.

    Input df columns required:
    ['Timeline', 'Simple Linear', 'Multiple Linear', 'Polynomial']

    Returns:
    - option (dict)
    """

    if df.empty:
        return {}

    timeline = df["Timeline"].tolist()
    simple_linear = df["Simple Linear"].tolist()
    multiple_linear = df["Multiple Linear"].tolist()
    polynomial = df["Polynomial"].tolist()

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"}
        },
        "legend": {
            "top": "2%",
            "data": ["Simple Linear", "Multiple Linear", "Polynomial"]
        },
        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": timeline
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "axisLabel": {
                "formatter": "₹{value}"
            }
        },
        "series": [
            {
                "name": "Simple Linear",
                "type": "bar",
                "data": simple_linear,
                "barGap": "15%",
                "itemStyle": {
                    "color": "#2563EB"  # Royal Blue
                }
            },
            {
                "name": "Multiple Linear",
                "type": "bar",
                "itemStyle": {
                    "color": "#16A34A"  # Emerald Green
                },
                "data": multiple_linear
            },
            {
                "name": "Polynomial",
                "type": "bar",
                "data": polynomial,
                "itemStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "#F59E0B"},  # Amber (positive)
                            {"offset": 1, "color": "#DC2626"}   # Red (negative)
                        ]
                    }
                }
            }
        ]
    }

    return option


def build_actual_vs_prediction_option(regression_results):
    """
    Builds an ECharts line chart for
    Actual vs Predicted Prices (Polynomial Regression)

    Expects:
    regression_results["polynomial"] = {
        "y_test": array-like,
        "y_pred": array-like
    }

    Returns:
    - option (dict)
    """

    poly_res = regression_results.get("multiple", {})
    y_test = poly_res.get("y_test", [])
    y_pred = poly_res.get("y_pred", [])

    if len(y_test) == 0 or len(y_pred) == 0:
        return {}

    # Ensure same length
    min_len = min(len(y_test), len(y_pred))
    y_test = y_test[:min_len]
    y_pred = y_pred[:min_len]

    # Convert NaN → None (JSON-safe)
    y_test = [None if pd.isna(v) else v for v in y_test]
    y_pred = [None if pd.isna(v) else v for v in y_pred]

    x_axis = list(range(min_len))

    option = {
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "top": "2%",
            "data": ["Actual", "Predicted (Polynomial)"]
        },
        "xAxis": {
            "type": "category",
            "data": x_axis,
            "name": "Test Sample Index"
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "name": "Price"
        },
        "series": [
            {
                "name": "Actual",
                "type": "line",
                "data": y_test,
                "smooth": False,
                "lineStyle": {
                    "width": 2.5,
                    "color": "#2563EB"  # Blue
                },
                "itemStyle": {
                    "color": "#2563EB"
                }
            },
            {
                "name": "Predicted (Polynomial)",
                "type": "line",
                "data": y_pred,
                "smooth": True,
                "lineStyle": {
                    "type": "dashed",
                    "width": 2.5,
                    "color": "#DC2626"  # Red
                },
                "itemStyle": {
                    "color": "#DC2626"
                }
            }
        ],
        "grid": {
            "left": "5%",
            "right": "5%",
            "top": "10%",
            "bottom": "10%",
            "containLabel": True
        }
    }

    return option


def rank_classification_models(clf_metrics_df):
    """
    Ranks classification models based on a weighted composite score.

    Expected columns:
    - Model
    - Accuracy
    - Precision (weighted)
    - Recall (weighted)
    - F1 (weighted)
    - AUC (OVR)

    Returns:
    - ranked DataFrame (best model on top)
    """

    if clf_metrics_df.empty:
        return pd.DataFrame()

    df = clf_metrics_df.copy()

    metric_cols = [
        "Accuracy",
        "Precision (weighted)",
        "Recall (weighted)",
        "F1 (weighted)",
        "AUC (OVR)",
    ]

    # Normalize metrics (0–1)
    for col in metric_cols:
        max_val = df[col].max()
        if max_val > 0:
            df[col + "_norm"] = df[col] / max_val
        else:
            df[col + "_norm"] = 0

    # Weighted composite score (F1 & AUC more important)
    df["Final_Score"] = (
        0.20 * df["Accuracy_norm"]
        + 0.15 * df["Precision (weighted)_norm"]
        + 0.15 * df["Recall (weighted)_norm"]
        + 0.30 * df["F1 (weighted)_norm"]
        + 0.20 * df["AUC (OVR)_norm"]
    )

    # Rank models
    ranked_df = df.sort_values("Final_Score", ascending=False).reset_index(drop=True)
    ranked_df.insert(0, "Rank", ranked_df.index + 1)

    return ranked_df

def build_classification_radar_option(clf_metrics_df):
    """
    Builds an ECharts radar chart option for classification model comparison.

    Expected columns:
    - Model
    - Accuracy
    - Precision (weighted)
    - Recall (weighted)
    - F1 (weighted)
    - AUC (OVR)

    Returns:
    - option (dict)
    """

    if clf_metrics_df.empty:
        return {}

    df = clf_metrics_df.copy().reset_index(drop=True)

    # Build radar series data
    series_data = []
    for _, row in df.iterrows():
        series_data.append(
            {
                "name": row["Model"],
                "value": [
                    row["Accuracy"],
                    row["Precision (weighted)"],
                    row["Recall (weighted)"],
                    row["F1 (weighted)"],
                    row["AUC (OVR)"],
                ],
            }
        )

    option = {
        "tooltip": {},
        "legend": {
            "bottom": 0,
            "data": df["Model"].tolist(),
        },
        "radar": {
            "radius": "65%",
            "indicator": [
                {"name": "Accuracy", "max": 1},
                {"name": "Precision", "max": 1},
                {"name": "Recall", "max": 1},
                {"name": "F1 Score", "max": 1},
                {"name": "AUC", "max": 1},
            ],
        },
        "series": [
            {
                "type": "radar",
                "data": series_data,
                "areaStyle": {"opacity": 0.18},
                "lineStyle": {"width": 2},
                "symbolSize": 6,
            }
        ],
    }

    return option


def build_best_model_confusion_matrix_option(ranked_df, classification_results):
    """
    Builds an ECharts heatmap option for the confusion matrix
    of the best classification model (ranked_df index 0).

    Inputs:
    - ranked_df: DataFrame (best model at index 0)
    - classification_results: dict containing models & label_encoder

    Returns:
    - option (dict)
    """

    if ranked_df.empty:
        return {}

    # Get best model name
    best_model = ranked_df.iloc[0]["Model"]
    model_res = classification_results["models"].get(best_model)
    if model_res is None:
        return {}

    cm = model_res.get("confusion_matrix")
    if cm is None:
        return {}

    label_encoder = classification_results["label_encoder"]
    labels = label_encoder.inverse_transform(
        np.arange(len(label_encoder.classes_))
    ).tolist()

    # Convert confusion matrix to heatmap data
    heatmap_data = []
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            heatmap_data.append([j, i, int(cm[i][j])])

    option = {
        "tooltip": {
            "position": "top"
        },
        "grid": {
            "top": "15%",
            "left": "12%",
            "right": "5%",
            "bottom": "10%"
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
            "max": int(np.max(cm)),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "0%"
        },
        "series": [
            {
                "name": "Confusion Matrix",
                "type": "heatmap",
                "data": heatmap_data,
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

    return option


def build_growth_comparison_bar_option(comp_df):
    """
    Builds ECharts bar chart for 30-day growth comparison.

    Required columns in comp_df:
    - name
    - growth_30d

    Returns:
    - option (dict)
    """

    if comp_df.empty:
        return {}

    names = comp_df["name"].tolist()
    growth = comp_df["growth_30d"].tolist()

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": "function(p){return p[0].name + '<br/>Growth: ' + p[0].value.toFixed(2) + '%';}"
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
            "name": "Growth 30d (%)",
            "scale": True
        },
        "series": [
            {
                "name": "30-Day Growth %",
                "type": "bar",
                "data": growth,
                "barWidth": "55%",
                "itemStyle": {
                    "color": "#2563EB"
                }
            }
        ],
        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "15%",
            "containLabel": True
        }
    }

    return option



def build_normalized_price_index_option(comparative_history, coin_id):
    """
    Builds ECharts line chart for normalized price index (last 30 days).

    comparative_history:
        dict -> { coin_id : DataFrame with ['date','price'] }

    Returns:
        option (dict)
    """

    if not comparative_history:
        return {}

    series = []
    dates_ref = None

    for cid, hist_df in comparative_history.items():
        df_tmp = hist_df.sort_values("date").tail(30)
        if df_tmp.empty:
            continue

        base_price = df_tmp["price"].iloc[0]
        if base_price <= 0:
            continue

        norm_values = (df_tmp["price"] / base_price).tolist()
        dates = df_tmp["date"].dt.strftime("%Y-%m-%d").tolist()

        if dates_ref is None:
            dates_ref = dates

        series.append(
            {
                "name": coin_id if cid == coin_id else cid,
                "type": "line",
                "data": norm_values,
                "smooth": True,
                "lineStyle": {"width": 2},
                "symbol": "circle",
                "symbolSize": 5
            }
        )

    if not series:
        return {}

    option = {
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "top": "2%"
        },
        "xAxis": {
            "type": "category",
            "data": dates_ref
        },
        "yAxis": {
            "type": "value",
            "name": "Normalized Index (1.0 = 30d Start)",
            "scale": True
        },
        "series": series,
        "grid": {
            "top": "15%",
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
            "containLabel": True
        }
    }

    return option
