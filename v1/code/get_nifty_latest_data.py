import requests
import pandas as pd

url = "https://api.upstox.com/v3/historical-candle/NSE_INDEX|Nifty 50/minutes/1/2025-07-26/2025-07-25"

payload={}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:
    data = response.json()

    candles = data['data']['candles']

    # Create a Pandas DataFrame
    df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'open_interest'])

    # Sort the DataFrame by time in ascending order
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values(by='time', ascending=True)
    # Save to CSV
    csv_file_path = '/Users/surajkumar/Documents/codebases/alpha_research/Project-V/data/nifty_minute_data.csv'
    df.to_csv(csv_file_path, index=False)

    print(f"Data saved to {csv_file_path}")
else:
    print(f"Error: {response.status_code} - {response.text}")