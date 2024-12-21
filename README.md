# Implied Volatility Surface Interactive App 🌌

An interactive Streamlit-based web application to visualize the **Implied Volatility Surface** for options of a specified ticker. This tool enables users to dynamically analyze implied volatility based on various parameters such as strike prices, moneyness, time to expiration, and more.

---

## 🚀 Features
- **Interactive Volatility Surface Visualization**:
  - 3D surface plots using Plotly for clear and engaging visuals.
  - Support for both **Moneyness** and **Strike Price** views.
- **Dynamic Inputs**:
  - Specify ticker symbols.
  - Set risk-free rate and dividend yield to customize calculations.
  - Define strike price ranges as a percentage of the spot price.
- **Data Processing**:
  - Fetches real-time stock and options data.
  - Calculates implied volatility dynamically for filtered options.
- **Customizable Display**:
  - Dark-themed UI for a sleek, modern look.
  - Sidebar options for personalized configurations.

---

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Processing**: `NumPy`, `SciPy`, `Pandas`
- **Visualization**: [Plotly](https://plotly.com/)
- **Options Data**: Custom `main.py` module for fetching and processing data

---

## 🎯 How It Works
1. **Input Parameters**:  
   Configure the ticker symbol, risk-free rate, dividend yield, and strike price/moneyness ranges using the sidebar.

2. **Fetch and Filter Data**:  
   - Real-time spot price is retrieved for the selected ticker.
   - Options data is filtered based on the configured parameters.

3. **Calculate Implied Volatility**:  
   Using a custom implementation in the `main.py` module, the implied volatility is calculated dynamically.

4. **Visualize the Surface**:  
   A 3D surface plot of implied volatility is displayed, with axes representing:
   - Time to Expiration (X)
   - Moneyness or Strike Price (Y)
   - Implied Volatility (Z)

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/implied-volatility-surface.git
cd implied-volatility-surface
```


## 🧩 File Structure

```plaintext
implied-volatility-surface/
│
├── app.py                # Main Streamlit app file
├── main.py               # Data processing and helper functions
├── requirements.txt      # Required Python libraries
└── README.md             # Project documentation


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check out the [issues page](https://github.com/yourusername/implied-volatility-surface/issues).

---

## 👨‍💻 Author

**Vinay Singh Yadav**  
Built with ❤️ and a passion for financial analysis.

---

## ✨ Acknowledgments

Thanks to [Streamlit](https://streamlit.io/) for providing an intuitive platform for building interactive applications.
