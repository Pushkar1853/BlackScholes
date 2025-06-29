# Black-Scholes Option Pricing & P&L Simulator

This repository provides an interactive Black-Scholes Pricing Model dashboard built using Streamlit. It allows users to **simulate and visualize both the option prices and the resulting P&L (Profit and Loss)** under varying market conditions.

Try it live:  
Refer site: [https://blackscholemodel.streamlit.app/](https://blackscholemodel.streamlit.app/)

---

## Features

### Options Pricing & P&L Heatmaps
- Visualizes **Call** and **Put** option prices using the **Black-Scholes formula**.
- Interactive **P&L heatmaps** help you analyze your **profit/loss** based on the option **purchase price** under different market scenarios.
- Color-coded heatmaps:
  - 🟩 **Green** for profit
  - 🟥 **Red** for loss

### Interactive Dashboard
- Real-time updates to all Black-Scholes model inputs:
  - Spot Price
  - Volatility
  - Strike Price
  - Time to Maturity
  - Risk-Free Interest Rate
  - Purchase Price of Call and Put options
- Dynamic heatmap ranges for Spot Price and Volatility.
- P&L heatmap generation is controlled via a button to avoid unnecessary recomputation.

### 🎯 Customizable Inputs
- Define your own market assumptions.
- Explore sensitivity to volatility and price swings.
- Simulate edge cases like zero volatility or expired options.

---

## How It Works

The app uses the **Black-Scholes formula** to calculate:
- Call and Put option prices
- Option Greeks (Delta and Gamma, used internally)
- Then computes **P&L** as:
  ```
  P&L = Black-Scholes Price – Purchase Price
  ```

The results are shown as a heatmap over a grid of:
- Varying **spot prices**
- Varying **volatilities**

---

## Dependencies

Make sure to install the following Python packages:

```bash
pip install streamlit numpy pandas matplotlib seaborn scipy plotly
```

---

## File Structure

```
📦blackscholes-pnl
 ┣ 📄 streamlit_app.py       ← Main Streamlit app file
 ┣ 📄 README.md              ← This file
```

## Author

[Pushkar Ambastha](https://www.linkedin.com/in/pushkar-ambastha/)  
Feel free to fork, contribute, or star the repo if you find it useful!

---
