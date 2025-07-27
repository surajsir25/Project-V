import pandas as pd

def calculate_ema_sma(df):
    # df['7sma'] = df['close'].rolling(window=7).mean()
    df['7ema'] = df['close'].ewm(span=7, adjust=False).mean()
    df['7ema_sma7'] = df['7ema'].rolling(window=7).mean()
    # df['7std'] = df['close'].rolling(window=7).std()
    # df['7min'] = df['close'].rolling(window=7).min()
    # df['7max'] = df['close'].rolling(window=7).max()
    # df['7median'] = df['close'].rolling(window=7).median()
    # df['7sum'] = df['close'].rolling(window=7).sum()
    # df['7roc'] = df['close'].pct_change(periods=7) * 100


    # Round to 2 decimal places
    df['7ema'] = df['7ema'].round(2)
    df['7ema_sma7'] = df['7ema_sma7'].round(2)

    # 7-period RSI (optional, simplified)
    # delta = df['close'].diff()
    # gain = delta.where(delta > 0, 0.0)
    # loss = -delta.where(delta < 0, 0.0)
    # avg_gain = gain.rolling(window=7).mean()
    # avg_loss = loss.rolling(window=7).mean()
    # rs = avg_gain / avg_loss
    # df['7rsi'] = 100 - (100 / (1 + rs))

    return df


df = pd.read_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/nfity_50_historical_minute_data.csv')

df = calculate_ema_sma(df)
df = df.dropna(axis=0)
df.to_csv('/Users/surajkumar/Documents/codebases/alpha_research/Project-V/v2/data/nifty_50_historical_minute_data_with_ema.csv', index=False)
print(df[['close', '7ema_sma7', '7ema']].head(10))
