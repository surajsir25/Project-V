import pandas as pd

# Load your data
df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/nifty_minute_data_with_ema.csv')

# Generate signals
df['signal'] = 0
df.loc[(df['7ema'] > df['7ema_sma7']) & (df['7ema'].shift(1) <= df['7ema_sma7'].shift(1)), 'signal'] = 1   # Buy
df.loc[(df['7ema'] < df['7ema_sma7']) & (df['7ema'].shift(1) >= df['7ema_sma7'].shift(1)), 'signal'] = -1  # Sell/Short

# Simulate trades
trades = []
position = 0  # 0 = flat, 1 = long, -1 = short
entry_time = None
entry_price = None
entry_action = None
entry_idx = None

for idx, row in df.iterrows():
    if row['signal'] == 1 and position <= 0:
        if position == -1:
            journey_df = df.loc[entry_idx:idx, ['time', 'close']].copy()
            journey_df['pnl'] = journey_df['close'].apply(lambda x: entry_price - x)
            journey = journey_df[['time', 'pnl']].to_dict('records')
            trades.append({
                'entry_time': entry_time,
                'exit_time': row['time'],
                'entry_action': entry_action,
                'exit_action': 'BUY',
                'entry_price': entry_price,
                'exit_price': row['close'],
                'pnl': entry_price - row['close'],
                'trade_journey': journey
            })
        entry_time = row['time']
        entry_price = row['close']
        entry_action = 'BUY'
        entry_idx = idx
        position = 1
    elif row['signal'] == -1 and position >= 0:
        if position == 1:
            journey_df = df.loc[entry_idx:idx, ['time', 'close']].copy()
            journey_df['pnl'] = journey_df['close'].apply(lambda x: x - entry_price)
            journey = journey_df[['time', 'pnl']].to_dict('records')
            trades.append({
                'entry_time': entry_time,
                'exit_time': row['time'],
                'entry_action': entry_action,
                'exit_action': 'SELL',
                'entry_price': entry_price,
                'exit_price': row['close'],
                'pnl': row['close'] - entry_price,
                'trade_journey': journey
            })
        entry_time = row['time']
        entry_price = row['close']
        entry_action = 'SELL'
        entry_idx = idx
        position = -1

# If a trade is open at the end, close it at the last price
if entry_time is not None and entry_price is not None:
    last_row = df.iloc[-1]
    journey_df = df.loc[entry_idx:df.index[-1], ['time', 'close']].copy()
    if position == 1:
        journey_df['pnl'] = journey_df['close'].apply(lambda x: x - entry_price)
        journey = journey_df[['time', 'pnl']].to_dict('records')
        trades.append({
            'entry_time': entry_time,
            'exit_time': last_row['time'],
            'entry_action': entry_action,
            'exit_action': 'SELL',
            'entry_price': entry_price,
            'exit_price': last_row['close'],
            'pnl': last_row['close'] - entry_price,
            'trade_journey': journey
        })
    elif position == -1:
        journey_df['pnl'] = journey_df['close'].apply(lambda x: entry_price - x)
        journey = journey_df[['time', 'pnl']].to_dict('records')
        trades.append({
            'entry_time': entry_time,
            'exit_time': last_row['time'],
            'entry_action': entry_action,
            'exit_action': 'BUY',
            'entry_price': entry_price,
            'exit_price': last_row['close'],
            'pnl': entry_price - last_row['close'],
            'trade_journey': journey
        })

# Output trades
trades_df = pd.DataFrame(trades)
print(trades_df[['entry_time', 'exit_time', 'entry_action', 'exit_action', 'pnl', 'trade_journey']])

# Save to CSV (trade_journey will be saved as a string)
trades_df.to_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades_with_journey.csv', index=False)