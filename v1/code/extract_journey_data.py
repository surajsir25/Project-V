import pandas as pd
import ast
import os

# Load trades with journey
trades_df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/ema_crossover_trades_with_journey.csv')

output_dir = '/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/trade_journeys'
os.makedirs(output_dir, exist_ok=True)

for i, row in trades_df.iterrows():
    journey = ast.literal_eval(row['trade_journey'])
    atp = float('-inf')
    lowest_retracement_pct = 0
    atp_list = []
    lowest_retracement_list = []
    for point in journey:
        pnl = point['pnl']
        time = point['time']
        if pnl > atp:
            atp = pnl
            lowest_retracement_pct = 0
        retracement = atp - pnl
        retracement_pct = (retracement / atp * 100) if atp != 0 else 0
        if retracement_pct > lowest_retracement_pct:
            lowest_retracement_pct = retracement_pct
        atp_list.append(round(atp, 2))
        lowest_retracement_list.append(round(lowest_retracement_pct, 2))
    out_df = pd.DataFrame({
        'time': [p['time'] for p in journey],
        'pnl': [round(p['pnl'], 2) for p in journey],
        'atp': atp_list,
        'lowest_retracement_pct': lowest_retracement_list
    })
    entry_time = row['entry_time']
    entry_epoch = int(pd.to_datetime(entry_time).timestamp())
    out_df.to_csv(f'{output_dir}/{entry_epoch}_trade_journey.csv', index=False)