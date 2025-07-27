import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v1/data/nifty_minute_data_with_ema.csv')

# Convert time column to datetime for better plotting
df['time'] = pd.to_datetime(df['time'])

plt.figure(figsize=(16, 8))
plt.plot(df['time'], df['close'], label='Close', color='black', linewidth=1)
plt.plot(df['time'], df['7ema'], label='7 EMA', color='blue', linewidth=1)
plt.plot(df['time'], df['7ema_sma7'], label='7 EMA SMA7', color='red', linewidth=1)

plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Nifty Minute Data with 7 EMA and 7 EMA SMA7')
plt.legend()
plt.tight_layout()
plt.show()