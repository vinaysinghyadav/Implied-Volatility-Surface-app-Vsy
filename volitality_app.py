import streamlit as st
import main as m
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go

# Enable Dark Theme through custom config
st.set_page_config(page_title="Implied Volatility Surface", layout="wide", page_icon="🌌")

# Apply additional custom styling for the app
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #444444;
        color: #FFFFFF;
        border: 1px solid #FFFFFF;
    }
    .stTextInput>div>input {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stNumberInput>div>input {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stSlider>div>div>div>div {
        background-color: #555555;
    }
    .sidebar .sidebar-content {
        background-color: #1c1c1c;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set up Streamlit app
st.title('Implied Volatility Surface Interactive App')
st.markdown("#### Made by Vinay Singh Yadav")

# Add sidebar logo and inputs
st.sidebar.header("User Inputs")
st.sidebar.image(
    "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
    use_container_width=True,  # Updated from `use_column_width` to `use_container_width`
)

# User Inputs
ticker = st.sidebar.text_input('Ticker', value='SPY')
risk_free_rate = st.sidebar.number_input('Risk-Free Rate', min_value=0.0, max_value=1.0, value=0.01, format="%.4f")
dividend_yield = st.sidebar.number_input('Dividend Yield', min_value=0.0, max_value=1.0, value=0.001, format="%.4f")

# User choice: Moneyness or Strike Price
option_type = st.sidebar.selectbox('Select Strike Price or Moneyness', ['Strike Price', 'Moneyness'])

# Retrieve the spot price dynamically to set up the slider range
stock, spot_prices, spot_price = m.get_stock_data(ticker)

# Set a dynamic percentage range for the slider to cover a broad enough strike price range
dynamic_min_percentage = 20  # 20% of the spot price
dynamic_max_percentage = 200  # 200% of the spot price

# Set a default range within the dynamic range
default_min_percentage = 70  # 70% of the spot price
default_max_percentage = 130  # 130% of the spot price

# Create the slider for strike price range percentages dynamically
strike_price_range_percentage = st.sidebar.slider(
    'Strike Price Range (as % of Spot Price)',
    min_value=dynamic_min_percentage,  # Minimum percentage allowed
    max_value=dynamic_max_percentage,  # Maximum percentage allowed
    value=(default_min_percentage, default_max_percentage)  # Default range
)

# Convert percentage range to fractions and calculate actual strike prices
min_percentage = strike_price_range_percentage[0] / 100
max_percentage = strike_price_range_percentage[1] / 100
min_strike_price = spot_price * min_percentage
max_strike_price = spot_price * max_percentage

# Get options data using the ticker specified by the user
calls_data, expiration_dates = m.get_options_data(stock)

# Filter the calls data using the calculated strike price range
filtered_calls_data = m.filter_calls_data(calls_data, spot_price, min_strike_price, max_strike_price)

# Calculate implied volatility with user-defined risk-free rate and dividend yield
imp_vol_data = m.calculate_implied_volatility(filtered_calls_data, spot_price, risk_free_rate, dividend_yield)

# Prepare data for plotting based on user selection
if option_type == 'Moneyness':
    # Calculate moneyness as Spot Price / Strike Price
    imp_vol_data['Moneyness'] = imp_vol_data['StrikePrice'] / spot_price
    X = imp_vol_data['TimeToExpiry'].values
    Y = imp_vol_data['Moneyness'].values
else:
    # Use Strike Price directly
    X = imp_vol_data['TimeToExpiry'].values
    Y = imp_vol_data['StrikePrice'].values

Z = imp_vol_data['ImpliedVolatility'].values * 100

# Check if data is available for plotting
if not X.size or not Y.size or not Z.size:
    st.error("No data available for the selected parameters. Please adjust your inputs.")
else:
    # Interpolate data for 3D surface plotting
    # Create a meshgrid for plotting
    xi = np.linspace(min(X), max(X), 30)
    yi = np.linspace(min(Y), max(Y), 30)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate Z values for the meshgrid
    zi = griddata((X, Y), Z, (xi, yi), method='linear')

    # Plot the data using Plotly
    fig = go.Figure(data=[go.Surface(x=xi, y=yi, z=zi, colorscale='Viridis')])
    fig.update_layout(
        title=f'Implied Volatility Surface of {ticker}',
        scene=dict(
            xaxis_title='Time to Expiration (years)',
            yaxis_title='Moneyness' if option_type == 'Moneyness' else 'Strike Price ($)',
            zaxis_title='Implied Volatility (%)'
        )
    )

    fig.update_layout(width=1000, height=800)  # Increase the plot size
    st.plotly_chart(fig)
