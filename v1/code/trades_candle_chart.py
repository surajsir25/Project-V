import pandas as pd
import matplotlib.pyplot as plt

# Load your trades data
trades_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades.csv')

# Calculate cumulative P&L
trades_df['cum_pnl_before'] = trades_df['pnl'].cumsum().shift(fill_value=0)
trades_df['cum_pnl_after'] = trades_df['cum_pnl_before'] + trades_df['pnl']
trades_df['color'] = trades_df['pnl'].apply(lambda x: 'green' if x > 0 else 'red')

plt.figure(figsize=(14, 6))
for idx, row in trades_df.iterrows():
    # Height and bottom for the bar
    height = row['cum_pnl_after'] - row['cum_pnl_before']
    bottom = row['cum_pnl_before']
    plt.bar(idx, height, bottom=bottom, color=row['color'], width=0.8, edgecolor='black')

plt.xlabel('Trade Number')
plt.ylabel('Cumulative Profit/Loss')
plt.title('Cumulative P&L by Trade (Green=Win, Red=Loss)')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()