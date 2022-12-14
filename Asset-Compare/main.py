import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

plt.style.use("dark_background")

"-----------------------------------------------"
def calculate_in_BTC_terms(df: pd.DataFrame, BTC_df: pd.DataFrame) -> pd.DataFrame:
    '''
    :param df: Dataframe of the primary asset.
    :param BTC_df: Dataframe of Bitcoin to compare to.
    :return: pd.Dataframe
    '''
    quotients = []
    for i in range(len(df['Adj Close'])):
        quotient = df['Adj Close'][i] / BTC_df['Adj Close'][i]
        quotients.append(quotient)

    df['BTC'] = quotients
    return df

"-----------------------------------------------"
def calculate_percent_change(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    '''
    :param df: Dataframe to perform the calculations on.
    :param column_name: The column name within the dataframe to calculate.
    :return: pd.DataFrame
    '''

    # Price of the beginning of the period.
    anchor = 0
    # Result of division between prices.
    quotient = 0
    # List to hold all of the quotients
    quotients = []

    print(f"DF: {df}   Columns: #")

    for i in range(len(df[column_name])):
        if i == 0:
            anchor = df[column_name][i]
            quotients.append(0)
        else:
            cur_number = df[column_name][i]

            # If it gained value between current period and starting period.
            if cur_number > anchor:
                # Formula for percentage increase
                quotient = ((cur_number - anchor) / anchor) * 100
            # If it lost value between current period and starting period.
            elif cur_number < anchor:
                # Formula for percentage decrease
                quotient = (((anchor - cur_number) / anchor) * 100) * -1
            quotients.append(quotient)
    # Determines which column to store data in.
    if column_name == "Adj Close":
        df['% Change'] = quotients
    elif column_name == "BTC":
        df['BTC % Change'] = quotients
    return df

"-----------------------------------------------"
def plot_asset_comparison(assets: list, period: str = "5Y", interval: str = "1d", in_BTC: bool = False, both: bool = False):
    '''
    :param assets: List of cryptocurrencies to compare.
    :param period: The window of time to plot.
    :param interval: The granularity of data.
    :param in_BTC: If the asset is being compared in terms of Bitcoin buying power.
    :param both: If the asset is being compared both in terms of United States Dollars and Bitcoin buying power.
    :return: None
    '''
    if both:
        if not in_BTC:
            in_BTC = True


    # Customize the dimensions of the graph
    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(111)

    # Declare variables
    df = None
    btc_df = None

    # If it is plotting in terms of Bitcoin, then it will download the relevant data regardless if it is in the asset list.
    if in_BTC:
       btc_df = yf.download("BTC-USD", period=period, interval=interval)

    # Loop through every asset.
    for asset in assets:
        print(f"Assets: {asset}")
        if asset == "BTC-USD":
            if in_BTC:
                df = btc_df
            else:
                df = yf.download(asset, period=period, interval=interval)
        elif asset != "BTC-USD":
            df = yf.download(asset, period=period, interval=interval)

        # If it is comparing in terms of USD and BTC.
        if both:
            ticker = None
            # Convert ticker to be in terms of BTC (ex. ETH-USD -> ETH-BTC)
            try:
                ticker = asset.split("-")[0]
                ticker = ticker + "-BTC"
            except ValueError:
                pass
            # Get percentage change between periods in terms of USD
            df = calculate_percent_change(df, column_name="Adj Close")
            df = calculate_in_BTC_terms(df, BTC_df=btc_df)

            df = calculate_percent_change(df, column_name="BTC")
            ax.plot(df["% Change"], label=asset)
            ax.plot(df["BTC % Change"], label=ticker)
        # If it is only comparing in terms of one currency.
        else:
            # If comparing in terms of BTC
            if in_BTC:
                ticker = None
                # Convert ticker to be in terms of BTC (ex. ETH-USD -> ETH-BTC)
                try:
                    ticker = asset.split("-")[0]
                    ticker = ticker + "-BTC"
                except ValueError:
                    pass
                df = calculate_in_BTC_terms(df, BTC_df=btc_df)
                df = calculate_percent_change(df, column_name="BTC")
                ax.plot(df["BTC % Change"], label=ticker)
            # If comparing in terms of USD
            elif not in_BTC:
                print(f"DF1111: {df}")
                df = calculate_percent_change(df, column_name="Adj Close")
                ax.plot(df["% Change"], label=asset)

    # Get the labels from the plots
    h, l = ax.get_legend_handles_labels()
    # Create a title for the graph.
    plt.title("Asset Comparison")
    # Rotate the x-axis labels.
    plt.xticks(rotation=45, horizontalalignment='right')
    # Create axis labels
    plt.xlabel("Years")
    plt.ylabel("% Change")
    # Create legend with the appropriate labels.
    plt.legend(l, loc="upper left")
    # Display figure
    plt.show()

"-----------------------------------------------"
def main():
    # List of assets to compare
    assets = ["Your list here",""]
    # Plots the assets
    plot_asset_comparison(assets, period="5Y", interval="1d", in_BTC=False, both=False)



""" Valid Period Parameters

1d, 5d, 1mo
3mo, 6mo, 1y
2y, 5y, 10y
ytd, max
"""

""" Valid Interval Parameters
1m, 2m, 5m, 
15m, 30m, 60m,
90m, 1h, 1d,
5d, 1wk, 1mo,
3mo
"""


main()
