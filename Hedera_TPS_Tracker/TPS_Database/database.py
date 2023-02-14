import os
import sqlite3
import datetime as dt


cwd = os.getcwd()


db_file = cwd + "\\TPS_Database\\hedera_tps.db"

print(f"FILE: {db_file}")


class TpsDatabase:
    def __init__(self) -> None:
        self.table_name = "HederaTPS"
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    '''-----------------------------------'''

    def create_table(self, table_name: str = None) -> None:
        # date: The date the data was collected.
        # time: The time the data was collected.
        # main_txn: The amount of transactions on the Hedera mainnet when the data was collected.
        # main_tps: The transactions per second on the Hedera mainnet.
        # test_txn: The amount of transaction on the Hedera testnet.
        # test_tps: The transactions per second on the Hedera testnet.
        # price: Price of HBAR at the time the data was collected.
        # marketcap: The market cap of HBAR.
        # rank: The market cap rank relative to other cryptocurrencies.
        # inBTC: HBAR in relative terms to Bitcoin.

        if table_name == None:
            table_name = self.table_name

        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS %s
                                (
                                    date TEXT,
                                    time TEXT,
                                    main_txn REAL,
                                    main_tps REAL,
                                    test_txn REAL,
                                    test_tps REAL,
                                    price REAL,
                                    marketcap REAL,
                                    rank REAL,
                                    tvl REAL,
                                    accounts REAL,
                                    inBTC REAL
                                )""" % table_name)

    '''-----------------------------------'''

    def insert_data(self, date: str, time: str, main_txn: int, main_tps: int, test_txn: int, test_tps: int, price: float, marketcap: int, rank: int, tvl: str, accounts: int, in_BTC: float):

        query_params = (date, time, main_txn, main_tps,
                        test_txn, test_tps, price, marketcap, rank, tvl, accounts, in_BTC)
        with self.conn:
            try:
                self.cur.execute(
                    """INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" % self.table_name, query_params)
            except sqlite3.IntegrityError:
                pass
            except sqlite3.OperationalError:
                self.create_table()
                self.insert_data(date, time, main_txn,
                                 main_tps, test_txn, test_tps,
                                 price, marketcap, rank, tvl, accounts, in_BTC)

    '''-----------------------------------'''

    def get_data_from_table(self) -> None:
        self.cur.execute("SELECT * FROM %s" % self.table_name)
        data = self.cur.fetchall()
        return data

    '''-----------------------------------'''

    def update_table_by_field(self, data_to_search: str, data_to_replace: str) -> None:
        '''
        Possible Fields:
        - date
        - time
        - main_txn
        - main_tps
        - test_txn
        - test_tps
        - price
        - marketcap
        - rank
        - inBTC
        '''
        with self.conn:
            self.cur.execute("""UPDATE %s SET test_txn = :replace WHERE time = :search""" % self.table_name, {
                             'replace': data_to_replace, 'search': data_to_search})
            # query = f"UPDATE {self.table_name} SET {field_to_replace} = {data_to_replace} WHERE {field_to_search} = {data_to_search}"
            # self.cur.execute(query)
            # print(f"- Successfully updated field: {field_to_replace}")

    '''-----------------------------------'''

    def insert_data_by_field(self, table_name: str = None, field: str = None, data_to_insert: int = 0, where_clause: str = None) -> None:

        if table_name == None:
            table_name = self.table_name

        with self.conn:
            self.cur.execute("""UPDATE %s SET rank = :replace WHERE date = :search""" % table_name, {
                             'replace': data_to_insert, 'search': where_clause})

    '''-----------------------------------'''

    def rename_table(self, original_table_name: str = None, new_table_name: str = None) -> None:
        # If there is no name passed, it will default to the class's table_name.
        if original_table_name == None:
            original_table_name = self.table_name
        with self.conn:
            query = f"ALTER TABLE {original_table_name} RENAME TO {new_table_name}"
            self.cur.execute(query)
            print(
                f"-- Table renamed from ({original_table_name}) to ({new_table_name})")

    '''-----------------------------------'''

    def delete_from_table_by_time(self, time) -> None:
        with self.conn:
            self.cur.execute("DELETE FROM %s WHERE time=(?)" %
                             self.table_name, (time,))

    '''-----------------------------------'''

    def delete_from_table_by_date(self, date) -> None:
        with self.conn:
            self.cur.execute("DELETE FROM %s WHERE date=(?)" %
                             self.table_name, (date,))
    '''-----------------------------------'''

    def wipe_table(self):
        with self.conn:
            self.cur.execute("DELETE FROM %s" % self.table_name)

    '''-----------------------------------'''

    def get_table(self, table_name: str = None):

        if table_name == None:
            table_name = self.table_name

        with self.conn:
            query = f"SELECT * FROM {table_name}"

            self.cur.execute(query)
            data = self.cur.fetchall()

            return data

    '''-----------------------------------'''

    def drop_table(self, table_name: str) -> None:

        usr_input = str(
            input(f' - Are you sure you want to drop table "{table_name}"(Y/N): '))

        if usr_input == "Y" or usr_input == "y":
            with self.conn:
                query = f"DROP TABLE {table_name}"
                self.cur.execute(query)
                print(f" -- Table ({table_name}) was dropped successfully")
        elif usr_input == "N" or usr_input == "n":
            print(f" -- Table drop aborted")
        elif usr_input != "Y" or usr_input != "y" or usr_input != "N" or usr_input != "n":
            print(f" -- Invalid input")
            self.drop_table(table_name)

    '''-----------------------------------'''

    def copy_table(self, table_to_copy: str, destination_table: str = None) -> None:

        # If no table name is passed, it will default to the class's table name.
        if destination_table == None:
            destination_table = self.table_name
        with self.conn:
            query = f"""INSERT INTO {destination_table} (
                                    date,
                                    time,
                                    main_txn,
                                    main_tps,
                                    test_txn,
                                    test_tps,
                                    price,
                                    marketcap,
                                    rank,
                                    tvl,
                                    inBTC
                                ) 
                        SELECT date, time, main_txn, main_tps, test_txn, test_tps, price, marketcap, rank, tvl, inBTC FROM {table_to_copy}"""

            self.cur.execute(query)

    '''-----------------------------------'''

    def rebuild_database_from_comment(self, comment: str) -> None:
        contents = comment.split("\n")
        # Reverse the contents of the comment so that it will be inputed to the database correctly.
        contents = list(reversed(contents))

        print(f'Contents: {contents}')
        for line in contents:

            data = line.split("|")

            if len(data) < 3:
                pass
            else:
                if "Date" in data or ":-" in data:
                    pass
                else:
                    # Extract the date.
                    date = data[1]
                    # Extract the time (in UTC).
                    time = data[2]

                    # Extract the main transactions. Replace the commas, and convert to integer. Try statement is to remove percentage change.
                    try:
                        main_txn = int(data[3].replace(",", ""))
                    except ValueError:
                        main_txn = int(str(main_txn).split(" ")[0])

                    # Extract the main tps. Convert to integer.
                    try:
                        main_tps = int(data[5])
                    except ValueError:
                        main_tps = int(str(main_tps).split(" ")[0])

                    # Extract the test transactions. Replace the commas, and convert to integer.
                    try:
                        test_txn = int(data[6].replace(",", ""))
                    except ValueError:
                        test_txn = int(str(test_txn).split(" ")
                                       [0].replace(",", ""))

                    # Extract the test tps. Convert to integer.
                    try:
                        test_tps = int(data[8])
                    except ValueError:
                        test_tps = int(str(test_tps).split(" ")[0])

                    # Extract the price. Slice off the dollar sign. Convert to float.
                    try:
                        price = float(data[9][1:])
                    except ValueError:
                        price = float(str(data[9][1:]).split(" ")[0])

                    # Extract the market cap and rank.
                    marketcap, rank = data[10].split(" ")

                    # Format the market cap to remove the dollar sign and comma.
                    marketcap = marketcap[1:].replace(",", "")

                    # Format the rank to remove the parenthesis and # symbol.
                    rank = rank[2:-1]

                    # Extract the tvl. Remove the commas and slice off the dollar sign.
                    try:
                        tvl = int(data[11][1:].replace(",", ""))
                    except ValueError:
                        try:
                            tvl = int(str(data[11][1:].split(" ")[0]))
                        # If this except statement is activated, then set the variable to 0.
                        except ValueError:
                            tvl = 0

                    # Extract the number of accounts. Remove the commas.
                    try:
                        accounts = int(data[12].replace(",", ""))
                    except ValueError:
                        try:
                            accounts = int(str(data[12].split(" ")))
                        except ValueError:
                            accounts = 0

                    # Extract the HBAR/BTC values.
                    inBTC = float(data[13].split(" ")[0])
                    inBTC = "{:.9f}".format(inBTC)

                    print(f"""
                    Date: {date}
                    Time: {time}
                    Main_TXN: {main_txn}
                    Main_TPS: {main_tps}
                    Test_TXN: {test_txn}
                    Test_TPS: {test_tps}
                    Price: {price}
                    Market cap: {marketcap}
                    Rank: {rank}
                    TVL: {tvl}
                    Accounts: {accounts}
                    HBAR/BTC: {inBTC}
                    """)
