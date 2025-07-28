import pandas as pd
import plotly.graph_objects as go

# Load your trades data
trades_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades.csv')

# Calculate cumulative P&L
trades_df['cum_pnl_before'] = trades_df['pnl'].cumsum().shift(fill_value=0)
trades_df['cum_pnl_after'] = trades_df['cum_pnl_before'] + trades_df['pnl']
trades_df['color'] = trades_df['pnl'].apply(lambda x: 'green' if x > 0 else 'red')

# Create interactive bar chart
fig = go.Figure()

for idx, row in trades_df.iterrows():
    fig.add_trace(go.Bar(
        x=[idx],
        y=[row['cum_pnl_after'] - row['cum_pnl_before']],
        base=row['cum_pnl_before'],
        marker_color=row['color'],
        width=0.8,
        name=f"Trade {idx+1}",
        hovertemplate=(
            f"Trade: {idx+1}<br>"
            f"Entry: {row.get('entry_time', '')}<br>"
            f"Exit: {row.get('exit_time', '')}<br>"
            f"PnL: {row['pnl']}<br>"
            f"Cumulative PnL: {row['cum_pnl_after']}"
        )
    ))

fig.update_layout(
    title='Cumulative P&L by Trade (Interactive)',
    xaxis_title='Trade Number',
    yaxis_title='Cumulative Profit/Loss',
    bargap=0.2,
    showlegend=False
)

fig.show()