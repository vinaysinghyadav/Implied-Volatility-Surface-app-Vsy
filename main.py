# main.py
import yfinance as yf
import pandas as pd
import numpy as np
import functions as f
import streamlit as st
from scipy.interpolate import griddata
import plotly.graph_objects as go


def get_stock_data(ticker_symbol="SPY", period="1y"):
    stock = yf.Ticker(ticker_symbol)
    spot_prices = stock.history(period=period)["Close"].to_frame()

    # Attempt to get today's spot price safely
    spot_data = stock.history(period="1d")["Close"]

    if not spot_data.empty:
        spot_price = spot_data.iloc[-1]
    else:
        st.warning(f"No recent data available for ticker {ticker_symbol}. Defaulting to last available price from historical data.")
        spot_price = spot_prices.iloc[-1, 0] if not spot_prices.empty else None

    if spot_price is None:
        raise ValueError(f"No data available for ticker {ticker_symbol}. Please check the ticker symbol or try again later.")
    
    return stock, spot_prices, spot_price


def get_options_data(stock):
    expiration_dates = stock.options
    calls_dict = {date: stock.option_chain(date).calls for date in expiration_dates}

    for date, df in calls_dict.items():
        df['expiration'] = date

    calls_all = pd.concat(calls_dict.values())
    return calls_all, expiration_dates

def filter_calls_data(calls_data, spot_price, min_strike_price, max_strike_price):
    filtered_calls_data = calls_data[(calls_data['strike'] >= min_strike_price) & (calls_data['strike'] <= max_strike_price)]
    filtered_calls_data = filtered_calls_data[filtered_calls_data['expiration'].apply(f.calculate_time_to_expiration) >= 0.07]

    return filtered_calls_data.reset_index(drop=True)

def calculate_implied_volatility(filtered_calls_data, spot_price, risk_free_rate, dividend_yield):
    imp_vol_data = pd.DataFrame(columns=["ContractSymbol", "StrikePrice", "TimeToExpiry", "ImpliedVolatility"])
    df_index = 0

    for i in range(len(filtered_calls_data)):
        if f.calculate_time_to_expiration(filtered_calls_data.iloc[i]["expiration"]) > 0:
            time_to_expiry = f.calculate_time_to_expiration(filtered_calls_data.iloc[i]["expiration"])
            imp = f.Call_IV(
                S=spot_price,
                X=filtered_calls_data.iloc[i]["strike"],
                r=risk_free_rate,
                T=time_to_expiry,
                Call_Price=filtered_calls_data.iloc[i]["lastPrice"],
                q=dividend_yield  # Assuming no dividend yield here; adjust if needed
            )
            imp_vol_data.loc[df_index] = [
                filtered_calls_data.iloc[i]['contractSymbol'],
                filtered_calls_data.iloc[i]["strike"],
                time_to_expiry,
                imp
            ]
            df_index += 1

    return imp_vol_data.dropna().reset_index(drop=True)

def get_plot_data(filtered_df):
    X = filtered_df['TimeToExpiry'].values
    Y = filtered_df['StrikePrice'].values
    Z = filtered_df['ImpliedVolatility'].values * 100

    return X, Y, Z

# Optional: a function to create the plot if needed.
def plot_implied_volatility(X, Y, Z):
    # Define grid for interpolation
    xi = np.linspace(X.min(), X.max(), 50)
    yi = np.linspace(Y.min(), Y.max(), 50)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate Z values over the grid
    zi = griddata((X, Y), Z, (xi, yi), method='linear')

    # Create the 3D plot using Plotly
    fig = go.Figure(data=[go.Surface(x=xi, y=yi, z=zi, colorscale='Viridis')])
    fig.update_layout(
        title='Implied Volatility Surface',
        scene=dict(
            xaxis_title='Time to Expiration (years)',
            yaxis_title='Strike Price ($)',
            zaxis_title='Implied Volatility (%)'
        )
    )

    return fig