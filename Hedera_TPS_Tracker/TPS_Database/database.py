import os
import sqlite3
import datetime as dt


cwd = os.getcwd()


db_file = "DIR"


class TpsDatabase:
    def __init__(self) -> None:
        self.table_name = "HederaTPS"
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    '''-----------------------------------'''

    def create_table(self) -> None:
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
                                    rank REAL
                                )""" % self.table_name)

    '''-----------------------------------'''

    def insert_data(self, date: str, time: str, main_txn: int, main_tps: int, test_txn: int, test_tps: int, price: float, marketcap: int, rank: int):

        query_params = (date, time, main_txn, main_tps,
                        test_txn, test_tps, price, marketcap, rank)
        with self.conn:
            try:
                self.cur.execute(
                    """INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""" % self.table_name, query_params)
            except sqlite3.IntegrityError:
                pass
            except sqlite3.OperationalError:
                self.create_table()
                self.insert_data(date, time, main_txn,
                                 main_tps, test_txn, test_tps)

    '''-----------------------------------'''

    def get_data_from_table(self):
        self.cur.execute("SELECT * FROM %s" % self.table_name)
        data = self.cur.fetchall()
        return data

    '''-----------------------------------'''

    def delete_from_table(self, time):
        with self.conn:
            self.cur.execute("DELETE FROM %s WHERE time=(?)" %
                             self.table_name, (time,))

    '''-----------------------------------'''

    def wipe_table(self):
        with self.conn:
            self.cur.execute("DELETE FROM %s" % self.table_name)
