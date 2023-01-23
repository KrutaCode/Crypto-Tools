import os
import time
import datetime as dt
from PIL import Image

# Database related imports
from TPS_Database.database import TpsDatabase

# Scraper related imports
from Scraper.scraper import TpsScraper

# Reddit related imports
from Reddit.reddit import RedditPoster

# Yahoo Finance
import yfinance as yf

cwd = os.getcwd()
screen_shot_path = cwd + "\\Scraper\\Screenshots\\"

'''-----------------------------------'''


def get_image_path() -> str:
    return screen_shot_path + "TPS_" + \
        str(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")) + ".png"


'''-----------------------------------'''


def get_price():
    ticker = "HBAR-USD"
    data = yf.download(ticker)['Adj Close'][-1]

    return data


'''-----------------------------------'''


def get_percent_change(starting_value, ending_value):

    try:
        starting_value = float(starting_value)
        ending_value = float(ending_value)
    except ValueError:
        # Case if numbers come in as a string with commas.
        if type(starting_value) == str:
            starting_value = starting_value.replace(",", "")
        if type(ending_value) == str:
            ending_value = ending_value.replace(",", "")

    try:
        starting_value, ending_value = float(
            starting_value), float(ending_value)
        pct_change = 0
        # If there was a percentage increase.
        if ending_value > starting_value:
            pct_change = ((ending_value - starting_value) /
                          abs(starting_value)) * 100

            pct_change = "{:.2f}".format(pct_change)

            # Determine symbol to place infront.
            if float(pct_change) >= 0:
                pct_change = "{:,}".format(float(pct_change))
                pct_change = "+" + str(pct_change) + "%"
            elif float(pct_change) < 0:
                pct_change = "{:,}".format(float(pct_change))
                pct_change = str(pct_change) + "%"
        # If there was a percentage decrease.
        elif ending_value < starting_value:
            pct_change = (((starting_value - ending_value) /
                           abs(starting_value)) * 100) * -1
            pct_change = "{:.2f}".format(pct_change)

            # Determine symbol to place infront.
            if float(pct_change) >= 0:
                pct_change = "{:,}".format(float(pct_change))
                pct_change = "+" + str(pct_change) + "%"
            elif float(pct_change) < 0:
                pct_change = "{:,}".format(float(pct_change))
                pct_change = str(pct_change) + "%"
        # If both values are equal
        elif ending_value == starting_value:
            pct_change = "-"
    # If there is no previous entry to compare.
    except ZeroDivisionError:
        pct_change = "-"
    except ValueError:
        pct_change = "-"

    return pct_change


'''-----------------------------------'''


def build_table(data):
    data = list(reversed(data))
    table = f"""
|Date|Time (UTC)|Main TXN|TXNs Added|Main TPS|Test TXN|TXNs Added|Test TPS|Price|Market Cap|
|:-|:-|:-|:-|:-|:-|:-|:-|-:|-:|
"""

    second_transaction_group = 0
    index = 0
    for i in range(len(data)):

        date = data[i][0]
        time = data[i][1]
        main_txn = data[i][2]
        main_tps = data[i][3]
        test_txn = data[i][4]
        test_tps = data[i][5]
        price = data[i][6]
        marketcap = data[i][7]
        rank = data[i][8]

        try:
            prev_main_txn = data[i+1][2]
            prev_main_tps = data[i+1][3]
            prev_test_txn = data[i+1][4]
            prev_test_tps = data[i+1][5]
            prev_price = data[i+1][6]

            main_transactions_added = main_txn - prev_main_txn
            test_transactions_added = test_txn - prev_test_txn
            main_tps_change = get_percent_change(
                starting_value=prev_main_tps, ending_value=main_tps)
            test_tps_change = get_percent_change(
                starting_value=prev_test_tps, ending_value=test_tps)
            price_pct_change = get_percent_change(
                starting_value=prev_price, ending_value=price)

            # Turn to integer to remove decimals
            main_transactions_added = int(main_transactions_added)
            test_transactions_added = int(test_transactions_added)

            # Format numbers with commas.
            main_transactions_added = "{:,}".format(main_transactions_added)
            test_transactions_added = "{:,}".format(test_transactions_added)
            index += 1
        # If there was no previous entry.
        except IndexError:
            main_transactions_added = "-"
            main_tps_change = "-"
            test_transactions_added = "-"
            test_tps_change = "-"
            price_pct_change = "-"
            print(f"Index")

        try:
            prev_prev_main_txn = data[i+2][2]
            prev_prev_test_txn = data[i+2][4]
            prev_main_transactions_added = prev_main_txn - prev_prev_main_txn
            prev_test_transactions_added = prev_test_txn - prev_prev_test_txn

            # Get the percentage change between rows.
            main_transactions_added_pct_change = get_percent_change(
                prev_main_transactions_added, main_transactions_added)
            test_transactions_added_pct_change = get_percent_change(
                prev_test_transactions_added, test_transactions_added)

        except IndexError:
            main_transactions_added_pct_change = "-"
            test_transactions_added_pct_change = "-"
            print("IndexError")

        # Convert to integers to remove decimal values
        main_txn, test_txn, main_tps, test_tps, marketcap, rank = int(
            main_txn), int(test_txn), int(main_tps), int(test_tps), int(marketcap), int(rank)

        # Add commas to transactions
        main_txn = "{:,}".format(main_txn)
        main_tps = "{:,}".format(main_tps)
        test_txn = "{:,}".format(test_txn)
        test_tps = "{:,}".format(test_tps)

        # If marketcap is 0, there is no entry. Therefore the variable will be set to "-".
        if marketcap == 0:
            marketcap = "-"
        else:
            # Add commas to field.
            marketcap = "{:,}".format(marketcap)
            # Format marketcap to have the ranking.
            marketcap = f"${marketcap} (#{rank})"

        # If marketcap is 0, there is no entry. Therefore the variable will be set to "-".
        if price == 0:
            price = "-"

        # If there is a previous entry, add the percent change to the string.
        if main_transactions_added_pct_change != "-":
            main_transactions_added = main_transactions_added + \
                f" ({main_transactions_added_pct_change})"
        # If a previous record is found, add the % change to the string.
        if test_transactions_added_pct_change != "-":
            test_transactions_added = test_transactions_added + \
                f" ({test_transactions_added_pct_change})"
        # If a previous record is found, add the % change to the string.
        if main_tps_change != "-":
            main_tps = main_tps + f" ({main_tps_change})"
        # If a previous record is found, add the % change to the string.
        if test_tps_change != "-":
            test_tps = test_tps + f" ({test_tps_change})"
        # Format the price % change to have a negative or positive sign, as well as adding the % change to the string.
        if price_pct_change != "-":
            price = f"${price}" + f" ({price_pct_change})"

        # If fields are zero put fill with "-".

        row = f"|{date}|{time}|{str(main_txn)}|{str(main_transactions_added)}|{main_tps}|{str(test_txn)}|{str(test_transactions_added)}|{str(test_tps)}|{price}|{marketcap}|\n"
        table += row
    return table


'''-----------------------------------'''


def visualize_table():

    db = TpsDatabase()
    data = db.get_data_from_table()
    table = build_table(data)

    print(f"Table: {table}")


'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''


def get_tps_figures(scraper: TpsScraper):
    scraper.create_browser()

    # It is possible to just return this statement without creating new variables. However we do this to give the scraper enough time to open up for the screenshot.
    main_txn, main_tps, test_txn, test_tps = scraper.get_mainnet_transactions(
    ), scraper.get_mainnet_tps(), scraper.get_testnet_transactions(), scraper.get_testnet_tps()
    # Capture screenshot of page.
    scraper.create_screenshot()

    return main_txn, main_tps, test_txn, test_tps


def get_tps_figures_test(scraper: TpsScraper):
    scraper.create_browser()

    # It is possible to just return this statement without creating new variables. However we do this to give the scraper enough time to open up for the screenshot.
    main_txn, main_tps, test_txn, test_tps = scraper.get_mainnet_transactions(
    ), scraper.get_mainnet_tps(), scraper.get_testnet_transactions(), scraper.get_testnet_tps()
    # Capture screenshot of page.
    scraper.create_screenshot()

    price, marketcap, rank = scraper.get_price(
    ), scraper.get_marketcap(), scraper.get_rank()

    return main_txn, main_tps, test_txn, test_tps, price, marketcap, rank


def main():
    start = time.time()
    tps = TpsScraper()
    db = TpsDatabase()

    # red = RedditPoster()
    img_path = get_image_path()

    utc_date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    utc_time = str(dt.datetime.now(dt.timezone.utc).time()).split(".")[0]

    # Get the data
    main_txn, main_tps, test_txn, test_tps, price, marketcap, rank = get_tps_figures_test(
        tps)

    db.insert_data(date=utc_date, time=utc_time, main_txn=main_txn,
                   main_tps=main_tps, test_txn=test_txn, test_tps=test_tps, price=price, marketcap=marketcap, rank=rank)

    # Get the data from the database.
    data = db.get_data_from_table()
    # Create a table for Reddit with the data.
    table = build_table(data=data)
    # Add the sources to the table.
    sources = "\n&#x200B;\n\nSources:\n\n[Network Activity](https://hederatxns.com/)\n\n[Price Data](https://coinmarketcap.com/currencies/hedera/)"
    table += sources

    # Create reddit object AFTER the scraper is done. Initializing the reddit object while the scraper is running will slow it down.
    red = RedditPoster()
    # print(
    #    f"\nMainnet: {main_txn}\nTPS: {main_tps}\n\nTestnet: {test_txn}\nTPS: {test_tps}")

    post_title = f"""Weekly Transaction Report: {utc_date} | {utc_time} AM UTC | (Table in comments)"""
    red.create_image_post(
        img_path=img_path, post_title=post_title, subreddit="Hedera", reply=table)

    stop = time.time()

    print(f"Elaspe: {stop - start}")


def test():
    db = TpsDatabase()
    db.delete_from_table("23:37:21")
    visualize_table()


main()



