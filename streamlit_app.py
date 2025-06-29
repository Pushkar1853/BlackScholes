import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import yfinance as yf

st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon='s',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}
.metric-call {
    background-color: #90ee90;
    color: black;
    margin-right: 10px;
    border-radius: 10px;
}
.metric-put {
    background-color: #ffcccb;
    color: black;
    border-radius: 10px;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}
.metric-label {
    font-size: 1rem;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

class BlackScholes:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(self):
        if self.time_to_maturity <= 0 or self.volatility <= 0:
            self.call_price = max(self.current_price - self.strike, 0)
            self.put_price = max(self.strike - self.current_price, 0)
            self.call_delta = self.put_delta = self.call_gamma = self.put_gamma = 0
            return self.call_price, self.put_price

        d1 = (log(self.current_price / self.strike) + (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * sqrt(self.time_to_maturity)

        self.call_price = self.current_price * norm.cdf(d1) - self.strike * exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)
        self.put_price = self.strike * exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - self.current_price * norm.cdf(-d1)

        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)
        self.call_gamma = self.put_gamma = norm.pdf(d1) / (self.current_price * self.volatility * sqrt(self.time_to_maturity))

        return self.call_price, self.put_price

with st.sidebar:
    st.title("Black Scholes Model")
    st.write('Created by:')
    st.markdown(f'''
    <a href="https://www.linkedin.com/in/pushkar-ambastha/" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px;">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" height="20" />
        <span style="font-size: 16px; font-weight: normal;">Pushkar Ambastha</span>
    </a>
    ''', unsafe_allow_html=True)

    st.markdown("### Load Real-Time Stock Price")
    ticker_symbol = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA):", value="AAPL")
    use_real_price = st.checkbox("Use Real-Time Price", value=True)

    try:
        ticker = yf.Ticker(ticker_symbol)
        current_price_live = ticker.history(period="1d")['Close'].iloc[-1]
        if use_real_price:
            st.success(f"Latest price for {ticker_symbol}: ${current_price_live:.2f}")
    except Exception as e:
        st.warning("Failed to fetch data for the ticker. Using default price.")
        current_price_live = 100.0

    current_price = st.number_input("Current Asset Price($S_{t}$)", value=float(current_price_live) if use_real_price else 100.0)
    strike = st.number_input("Strike Price (K)", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (t)(Years)", value=1.0)
    volatility = st.number_input("Volatility (\u03c3)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate (r)", value=0.05)
    call_purchase_price = st.number_input("Purchase Price of CALL Option", value=5.0)
    put_purchase_price = st.number_input("Purchase Price of PUT Option", value=5.0)

    st.markdown('----')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', 0.01, 1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', 0.01, 1.0, value=volatility*1.5, step=0.01)
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

def plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, call_price_paid, put_price_paid):
    call_pnl = np.zeros((len(vol_range), len(spot_range)))
    put_pnl = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            temp_model = BlackScholes(bs_model.time_to_maturity, strike, spot, vol, bs_model.interest_rate)
            temp_model.calculate_prices()
            call_pnl[i, j] = temp_model.call_price - call_price_paid
            put_pnl[i, j] = temp_model.put_price - put_price_paid

    cmap = mcolors.LinearSegmentedColormap.from_list("pnl_map", ["green", "white", "red"], N=100)

    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap=cmap, ax=ax_call)
    ax_call.set_title("CALL P&L")

    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap=cmap, ax=ax_put)
    ax_put.set_title("PUT P&L")

    return fig_call, fig_put

st.title("Black-Scholes Pricing Model")
bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()

st.table(pd.DataFrame({
    'Current Asset Price': [current_price],
    'Strike Price': [strike],
    'Time to Maturity (Years)': [time_to_maturity],
    'Volatility (\u03c3)': [volatility],
    'Risk-Free Interest Rate': [interest_rate]
}))

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="metric-container metric-call">
        <div>
            <div class="metric-label">CALL Value</div>
            <div class="metric-value">${call_price:.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container metric-put">
        <div>
            <div class="metric-label">PUT Value</div>
            <div class="metric-value">${put_price:.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)

st.title("Profit & Loss Heatmap")
if st.button("Generate P&L Heatmap"):
    fig_call, fig_put = plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, call_purchase_price, put_purchase_price)
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig_call)
    with col2:
        st.pyplot(fig_put)

if ticker_symbol:
    try:
        option_chain = ticker.option_chain()
        st.subheader("Sample Option Chain - Calls")
        st.dataframe(option_chain.calls[['strike', 'lastPrice', 'impliedVolatility']].head())
    except Exception:
        st.warning("Option chain data unavailable.")
