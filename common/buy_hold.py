import pandas as pd
import numpy as np

def implement_strategy(df):
    """
    Implements a trading strategy based on 7-period EMA and SMA crossovers.

    Args:
        df (pd.DataFrame): DataFrame containing candlestick data with 'Close' column.

    Returns:
        pd.DataFrame: DataFrame with added columns for EMA, SMA, and trading signals.
    """

    # Calculate 7-period EMA and SMA
    df['7EMA'] = df['Close'].ewm(span=7, adjust=False).mean()
    df['7SMA'] = df['Close'].rolling(window=7).mean()

    # Generate trading signals based on crossovers
    df['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
    df['Position'] = 0  # Current position: 0, 1 (Long)

    for i in range(1, len(df)):
        if df['7EMA'][i] > df['7SMA'][i] and df['7EMA'][i-1] <= df['7SMA'][i-1] and df['Position'][i-1] == 0:
            # 7EMA crosses above 7SMA (Buy signal)
            df['Signal'][i] = 1
            df['Position'][i] = 1  # Enter Long position
        elif df['7EMA'][i] < df['7SMA'][i] and df['7EMA'][i-1] >= df['7SMA'][i-1] and df['Position'][i-1] == 1:
            # 7EMA crosses below 7SMA (Sell signal)
            df['Signal'][i] = -1
            df['Position'][i] = 0  # Exit Long position
        else:
            # Hold current position
            df['Signal'][i] = 0
            df['Position'][i] = df['Position'][i-1]

    return df

# Example usage (assuming your CSV data is in a DataFrame called 'nifty_data')
# nifty_data = pd.read_csv('your_nifty_data.csv')  # Replace 'your_nifty_data.csv' with your actual file
# nifty_data = implement_strategy(nifty_data)
# print(nifty_data)
