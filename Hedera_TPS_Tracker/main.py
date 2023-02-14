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


cwd = os.getcwd()
screen_shot_path = cwd + "\\Scraper\\Screenshots\\"

test_subreddit = "BotTestingEnv"
hedera_subreddit = "Hedera"

'''-----------------------------------'''


def get_image_path() -> str:
    return screen_shot_path + "TPS_" + \
        str(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")) + ".png"


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
|Date|Time (UTC)|Main TXN|TXNs Added|Main TPS|Test TXN|TXNs Added|Test TPS|Price|Market Cap|TVL|Accounts|HBAR/BTC|
|:-|:-|:-|:-|:-|:-|:-|:-|-:|-:|-:|-:|-:|
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
        price = "{:.4f}".format(price)
        marketcap = data[i][7]
        rank = data[i][8]
        tvl = data[i][9]
        accounts = data[i][10]
        hbar_btc = data[i][11]
        hbar_btc = "{:.9f}".format(hbar_btc)

        try:
            prev_main_txn = data[i+1][2]
            prev_main_tps = data[i+1][3]
            prev_test_txn = data[i+1][4]
            prev_test_tps = data[i+1][5]
            prev_price = data[i+1][6]
            prev_tvl = data[i+1][9]
            prev_accounts = data[i+1][10]
            prev_hbar_btc = data[i+1][11]
            prev_hbar_btc = "{:.9f}".format(prev_hbar_btc)

            main_transactions_added = main_txn - prev_main_txn
            test_transactions_added = test_txn - prev_test_txn
            main_txn_pct_change = get_percent_change(
                starting_value=prev_main_txn, ending_value=main_txn)
            main_tps_change = get_percent_change(
                starting_value=prev_main_tps, ending_value=main_tps)
            test_txn_pct_change = get_percent_change(
                starting_value=prev_test_txn, ending_value=test_txn)
            test_tps_change = get_percent_change(
                starting_value=prev_test_tps, ending_value=test_tps)
            price_pct_change = get_percent_change(
                starting_value=prev_price, ending_value=price)
            tvl_pct_change = get_percent_change(
                starting_value=prev_tvl, ending_value=tvl)
            accounts_pct_change = get_percent_change(
                starting_value=prev_accounts, ending_value=accounts)
            hbar_btc_pct_change = get_percent_change(
                starting_value=prev_hbar_btc, ending_value=hbar_btc)

            # Turn to integer to remove decimals
            main_transactions_added = int(main_transactions_added)
            test_transactions_added = int(test_transactions_added)

            # Format numbers with commas.
            main_transactions_added = "{:,}".format(main_transactions_added)
            test_transactions_added = "{:,}".format(test_transactions_added)
            index += 1
        # If there was no previous entry.
        except IndexError:
            main_txn_pct_change = "-"
            main_transactions_added = "-"
            main_tps_change = "-"
            test_txn_pct_change = "-"
            test_transactions_added = "-"
            test_tps_change = "-"
            price_pct_change = "-"
            tvl_pct_change = "-"
            accounts_pct_change = "-"
            hbar_btc_pct_change = "-"

        try:
            # Calculate the row 2 before the current one.
            prev_prev_main_txn = data[i+2][2]
            prev_prev_test_txn = data[i+2][4]
            prev_main_transactions_added = prev_main_txn - prev_prev_main_txn
            prev_test_transactions_added = prev_test_txn - prev_prev_test_txn

            # Get the percentage change between rows.
            main_transactions_added_pct_change = get_percent_change(
                prev_main_transactions_added, main_transactions_added)
            test_transactions_added_pct_change = get_percent_change(
                prev_test_transactions_added, test_transactions_added)
        # If there was no previous entry.
        except IndexError:
            main_transactions_added_pct_change = "-"
            test_transactions_added_pct_change = "-"

        # Convert to integers to remove decimal values
        main_txn, test_txn, main_tps, test_tps, marketcap, rank, tvl, accounts = int(
            main_txn), int(test_txn), int(main_tps), int(test_tps), int(marketcap), int(rank), int(tvl), int(accounts)

        # Add commas to transactions
        main_txn = "{:,}".format(main_txn)
        main_tps = "{:,}".format(main_tps)
        test_txn = "{:,}".format(test_txn)
        test_tps = "{:,}".format(test_tps)

        # If price is 0, there is no entry. Therefore the variable will be set to "-".
        if price == 0:
            price = "-"

        # If marketcap is 0, there is no entry. Therefore the variable will be set to "-".
        if marketcap == 0:
            marketcap = "-"
        else:
            # Add commas to field.
            marketcap = "{:,}".format(marketcap)
            # Format marketcap to have the ranking.
            marketcap = f"${marketcap} (#{rank})"

         # If tvl = 0, there is no entry.
        if tvl == 0:
            tvl = "-"
        elif tvl != 0:
            # Add commas to the field.
            tvl = "{:,}".format(tvl)
            # Format the tvl.
            tvl = f"${tvl}"

        if accounts == 0:
            accounts = "-"
        elif accounts != 0:
            # Add commas to field.
            accounts = "{:,}".format(accounts)

        if main_txn_pct_change != "-":
            main_txn = main_txn + f" ({main_txn_pct_change})"
        if test_txn_pct_change != "-":
            test_txn = test_txn + f" ({test_txn_pct_change})"
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
        # Add the % change to the string.
        if price_pct_change != "-":
            price = f"{price}" + f" ({price_pct_change})"
        # Add the % change to the string.
        if tvl_pct_change != "-":
            tvl = f"{tvl}" + f" ({tvl_pct_change})"
        if accounts_pct_change != "-":
            accounts = f"{accounts}" + f" ({accounts_pct_change})"
        # Add the % change to the string.
        if hbar_btc_pct_change != "-":
            hbar_btc = f"{hbar_btc} BTC" + f" ({hbar_btc_pct_change})"
        elif hbar_btc_pct_change == "-":
            hbar_btc = f"{hbar_btc} BTC"

        # If fields are zero put fill with "-".

        row = f"|{date}|{time}|{str(main_txn)}|{str(main_transactions_added)}|{main_tps}|{str(test_txn)}|{str(test_transactions_added)}|{str(test_tps)}|${price}|{marketcap}|{tvl}|{accounts}|{hbar_btc}|\n"
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


def get_coin_data(scraper: TpsScraper):
    scraper.create_browser()

    # It is possible to just return this statement without creating new variables. However we do this to give the scraper enough time to open up for the screenshot.
    main_txn, main_tps, test_txn, test_tps = scraper.get_mainnet_transactions(
    ), scraper.get_mainnet_tps(), scraper.get_testnet_transactions(), scraper.get_testnet_tps()
    # Capture screenshot of page.
    scraper.create_screenshot()

    price, marketcap, rank, hbar_btc = scraper.get_price(
    ), scraper.get_marketcap(), scraper.get_rank(), scraper.get_in_BTC()

    tvl = scraper.get_tvl()
    accounts = scraper.get_accounts()

    return main_txn, main_tps, test_txn, test_tps, price, marketcap, rank, tvl, accounts, hbar_btc


def main():
    start = time.time()
    tps = TpsScraper()
    db = TpsDatabase()

    img_path = get_image_path()

    utc_date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    utc_time = str(dt.datetime.now(dt.timezone.utc).time()).split(".")[0]

    # Get the data
    main_txn, main_tps, test_txn, test_tps, price, marketcap, rank, tvl, accounts, hbar_btc = get_coin_data(
        tps)

    db.insert_data(date=utc_date, time=utc_time, main_txn=main_txn,
                   main_tps=main_tps, test_txn=test_txn, test_tps=test_tps, price=price, marketcap=marketcap, rank=rank, tvl=tvl, accounts=accounts, in_BTC=hbar_btc)

    # Get the data from the database.
    data = db.get_data_from_table()
    # Create a table for Reddit with the data.
    table = build_table(data=data)
    # Add the sources to the table.
    sources = "\n&#x200B;\n\nSources:\n\n[Network Activity](https://hederatxns.com/)\n\n[Price Data](https://coinmarketcap.com/currencies/hedera/)\n\n[Total Value Locked(TVL)](https://defillama.com/chain/Hedera)\n\n[Accounts](https://app.dragonglass.me/hedera/home)"
    table += sources

    # Create reddit object AFTER the scraper is done. Initializing the reddit object while the scraper is running will slow it down.
    red = RedditPoster()

    post_title = f"""Weekly Transaction Report: {utc_date} | (Table in comments)"""
    # red.create_image_post(
    #   img_path=img_path, post_title=post_title, subreddit=hedera_subreddit, reply=table)

    stop = time.time()

    print(f"Elaspe: {stop - start}")


def test():
    red = RedditPoster()
    db = TpsDatabase()

    comment = red.get_comment(
        "https://www.reddit.com/r/Hedera/comments/110u71d/weekly_transaction_report_20230213_table_in/")

    db.rebuild_database_from_comment(comment)


test()
'''
Checklist to make a Reddit post. 

1. Is the subreddit, to the correct one?
2. Is the flair_id to the correct flair?
3. Does the table look correct?





'''
