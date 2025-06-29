# Black-Scholes Option Pricing & P&L Simulator

This repository provides an interactive Black-Scholes Pricing Model dashboard built using Streamlit. It allows users to simulate and visualize both the option prices and the resulting P&L (Profit and Loss) under varying market conditions, using real-time market data from `yfinance`.

**Live App**: [https://blackscholemodel.streamlit.app/](https://blackscholemodel.streamlit.app/)

---

## Features

### Options Pricing, P&L, and Risk Heatmaps
- Computes **Call** and **Put** option prices using the Black-Scholes formula.
- Visualizes **P&L heatmaps** across a grid of spot prices and volatilities.
- Compares model prices to **real market option prices**, showing pricing errors as a heatmap.
- Visualizes **option Greeks** (Delta and Gamma) as 2D surfaces.

### Real-Time Market Data Integration
- Pulls the latest price data and option chain from `yfinance`.
- Allows users to simulate pricing using implied volatility and market strikes.

### Interactive Dashboard
- Fully adjustable inputs:
  - Spot Price (St)
  - Strike Price (K)
  - Volatility (σ)
  - Time to Maturity (t)
  - Risk-Free Rate (r)
  - Option purchase price
- Choose whether to use real-time data or manual inputs.
- Dynamically update the spot/volatility ranges for grid-based simulations.

---

## How It Works

The app calculates:

- Black-Scholes option prices
- Option Greeks (Delta, Gamma)
- P&L surface as:
  ```
  P&L = Model Option Price – Purchase Price
  ```
- Pricing Error as:
  ```
  Pricing Error = Model Price – Market Price
  ```

These are plotted over a configurable grid of:
- Spot Prices (S)
- Volatility (σ)

---

## Preview

![Pricing Heatmap Example](https://miro.medium.com/v2/resize:fit:904/1*82ZaRKWa3gUCCdTrZGeUlQ.png)  
*Black-Scholes theoretical pricing structure*

---

## Installation

```bash
pip install streamlit numpy pandas matplotlib seaborn scipy plotly yfinance
```

Run the app with:

```bash
streamlit run streamlit_app.py
```

---

## File Structure

```
📦 blackscholes/
 ┣ 📄 streamlit_app.py       # Main Streamlit dashboard
 ┣ 📄 README.md              # This file
```

---

## Author

**Pushkar Ambastha**  
[LinkedIn Profile](https://www.linkedin.com/in/pushkar-ambastha/)

---

