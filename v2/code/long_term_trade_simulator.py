import pandas as pd

# Load your data
df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/nifty_50_historical_minute_data_with_ema.csv')

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

for idx, row in df.iterrows():
    if row['signal'] == 1 and position <= 0:
        # Close short if open
        if position == -1:
            trades.append({
                'entry_time': entry_time,
                'exit_time': row['time'],
                'entry_action': entry_action,
                'exit_action': 'BUY',
                'entry_price': entry_price,
                'exit_price': row['close'],
                'pnl': entry_price - row['close']  # Short: sell high, buy low
            })
        # Open long
        entry_time = row['time']
        entry_price = row['close']
        entry_action = 'BUY'
        position = 1
    elif row['signal'] == -1 and position >= 0:
        # Close long if open
        if position == 1:
            trades.append({
                'entry_time': entry_time,
                'exit_time': row['time'],
                'entry_action': entry_action,
                'exit_action': 'SELL',
                'entry_price': entry_price,
                'exit_price': row['close'],
                'pnl': row['close'] - entry_price  # Long: buy low, sell high
            })
        # Open short
        entry_time = row['time']
        entry_price = row['close']
        entry_action = 'SELL'
        position = -1

# If a trade is open at the end, close it at the last price
if entry_time is not None and entry_price is not None:
    last_row = df.iloc[-1]
    if position == 1:
        trades.append({
            'entry_time': entry_time,
            'exit_time': last_row['time'],
            'entry_action': entry_action,
            'exit_action': 'SELL',
            'entry_price': entry_price,
            'exit_price': last_row['close'],
            'pnl': last_row['close'] - entry_price
        })
    elif position == -1:
        trades.append({
            'entry_time': entry_time,
            'exit_time': last_row['time'],
            'entry_action': entry_action,
            'exit_action': 'BUY',
            'entry_price': entry_price,
            'exit_price': last_row['close'],
            'pnl': entry_price - last_row['close']
        })

# Output trades
trades_df = pd.DataFrame(trades)
print(trades_df)

# Calculate totals
total_profit = trades_df['pnl'].sum()
total_profit_trades = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
total_loss_trades = trades_df[trades_df['pnl'] < 0]['pnl'].sum()

print(f"\nTotal P&L: {total_profit:.2f}")
print(f"Total Profit: {total_profit_trades:.2f}")
print(f"Total Loss: {total_loss_trades:.2f}")

# Save to CSV
trades_df.to_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/ema_crossover_trades.csv', index=False)