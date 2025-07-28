import pandas as pd
import numpy as np

# Load your trade data (assume you have columns: entry_time, exit_time, entry_price, exit_price, pnl)
trades_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades.csv')

# Win-Loss Ratio
wins = trades_df[trades_df['pnl'] > 0].shape[0]
losses = trades_df[trades_df['pnl'] < 0].shape[0]
win_loss_ratio = wins / losses if losses > 0 else np.nan

# Drawdown calculation
trades_df['cum_pnl'] = trades_df['pnl'].cumsum()
trades_df['cum_max'] = trades_df['cum_pnl'].cummax()
trades_df['drawdown'] = trades_df['cum_pnl'] - trades_df['cum_max']
max_drawdown = trades_df['drawdown'].min()

# Sharpe Ratio (assume risk-free rate = 0, use trade P&L as returns)
if trades_df['pnl'].std() != 0:
    sharpe_ratio = trades_df['pnl'].mean() / trades_df['pnl'].std() * np.sqrt(len(trades_df))
else:
    sharpe_ratio = np.nan

# Profit Factor
gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
gross_loss = -trades_df[trades_df['pnl'] < 0]['pnl'].sum()
profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.nan

# Round columns to 2 decimal places before saving
trades_df = trades_df.round({'pnl': 2, 'cum_pnl': 2, 'cum_max': 2, 'drawdown': 2})

# Print results
print(f"Win-Loss Ratio: {win_loss_ratio:.2f}")
print(f"Max Drawdown: {max_drawdown:.2f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Profit Factor: {profit_factor:.2f}")

# Optionally, save the trades with drawdown info
trades_df.to_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades_with_stats.csv', index=False)