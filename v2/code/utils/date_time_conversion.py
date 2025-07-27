import pandas as pd

# Load your data
df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/nfity_50_historical_minute_data.csv')

# Convert 'time' to datetime and localize to Asia/Kolkata (IST, +05:30)
df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].dt.tz_localize('Asia/Kolkata', ambiguous='NaT', nonexistent='shift_forward')

# Format as string with offset
df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S%z')
df['time'] = df['time'].str[:-2] + ':' + df['time'].str[-2:]  # Insert colon in +0530 → +05:30

# Save to new CSV
df.to_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/nfity_50_historical_minute_data.csv', index=False)