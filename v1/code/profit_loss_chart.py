import pandas as pd
import mplfinance as mpf

# Load price data
price_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/nifty_minute_data.csv')
price_df['time'] = pd.to_datetime(price_df['time'])
price_df.set_index('time', inplace=True)

# Load trades data
trades_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades.csv')

# Prepare buy/sell marker series
buy_marker = pd.Series(index=price_df.index, dtype=float)
sell_marker = pd.Series(index=price_df.index, dtype=float)

for _, row in trades_df.iterrows():
    entry_time = pd.to_datetime(row['entry_time'])
    if row['entry_action'] == 'BUY' and entry_time in price_df.index:
        buy_marker.loc[entry_time] = price_df.loc[entry_time, 'low'] - 10
    elif row['entry_action'] == 'SELL' and entry_time in price_df.index:
        sell_marker.loc[entry_time] = price_df.loc[entry_time, 'high'] + 10

addplots = [
    mpf.make_addplot(buy_marker, type='scatter', markersize=100, marker='^', color='g'),
    mpf.make_addplot(sell_marker, type='scatter', markersize=100, marker='v', color='r')
]

# Plot candlestick chart with trade markers
mpf.plot(
    price_df,
    type='candle',
    style='charles',
    title='EMA Crossover Trades',
    ylabel='Price',
    addplot=addplots,
    volume=False,
    figsize=(16, 8),
    tight_layout=True,
    show_nontrading=True
)