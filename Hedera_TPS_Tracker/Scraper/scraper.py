import os
import time
import datetime as dt
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


import requests
from bs4 import BeautifulSoup


hedera_txns = "https://hederatxns.com/"
coinmarketcap = "https://coinmarketcap.com/currencies/hedera/"

cwd = os.getcwd()
chrome_driver = cwd + "\\Scraper\\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')


class TpsScraper:
    def __init__(self) -> None:
        # Declare variables
        self.hedera_txns_url = "https://hederatxns.com/"
        self.coinmarketcap_url = "https://coinmarketcap.com/currencies/hedera/"

        self.mainet_tps = None
        self.testnet_tps = None
        self.mainnet_txn = None
        self.testnet_txn = None
        self.market_cap = None
        self.price = None
        self.rank = None

       # time.sleep(500)

    '''-----------------------------------'''

    def set_mainnet_transactions(self) -> None:
        if self.browser.current_url != self.hedera_txns_url:
            self._redirect_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/span[1]"
        self.mainnet_txn = int(self.read_data_wait(
            xpath=xpath).replace(",", ""))

    '''-----------------------------------'''

    def set_mainnet_tps(self) -> None:
        if self.browser.current_url != self.hedera_txns_url:
            self._redirect_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/span[2]"
        self.mainet_tps = int(self.read_data_wait(
            xpath=xpath).split(" ")[0][1:])

    '''-----------------------------------'''

    def set_testnet_transactions(self) -> None:
        if self.browser.current_url != self.hedera_txns_url:
            self._redirect_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/span[1]"
        self.testnet_txn = int(self.read_data_wait(
            xpath=xpath).replace(",", ""))

    '''-----------------------------------'''

    def set_testnet_tps(self) -> None:
        if self.browser.current_url != self.hedera_txns_url:
            self._redirect_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/span[2]"
        self.testnet_tps = int(self.read_data_wait(
            xpath=xpath).split(" ")[0][1:])
    '''-----------------------------------'''

    def set_marketcap(self) -> None:
        if self.browser.current_url != self.coinmarketcap_url:
            self._redirect_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div"
        self.market_cap = float(
            self.read_data_wait(xpath).replace(",", "")[1:])

    '''-----------------------------------'''

    def set_price(self) -> None:
        if self.browser.current_url != self.coinmarketcap_url:
            self._redirect_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span"
        self.price = float(self.read_data_wait(xpath)[1:])

    '''-----------------------------------'''

    def set_rank(self) -> None:
        if self.browser.current_url != self.coinmarketcap_url:
            self._redirect_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]"
        self.rank = int(self.read_data_wait(xpath).split(" ")[1][1:])

    '''-----------------------------------'''

    def get_mainnet_transactions(self) -> int:
        if self.mainnet_txn == None:
            self.set_mainnet_transactions()
        return self.mainnet_txn

    '''-----------------------------------'''

    def get_mainnet_tps(self) -> int:
        if self.mainet_tps == None:
            self.set_mainnet_tps()
        return self.mainet_tps

    '''-----------------------------------'''

    def get_testnet_transactions(self) -> int:
        if self.testnet_txn == None:
            self.set_testnet_transactions()
        return self.testnet_txn

    '''-----------------------------------'''

    def get_testnet_tps(self) -> int:
        if self.testnet_tps == None:
            self.set_testnet_tps()
        return self.testnet_tps

    '''-----------------------------------'''

    def get_marketcap(self) -> str:
        if self.market_cap == None:
            self.set_marketcap()
        return self.market_cap

    '''-----------------------------------'''

    def get_price(self) -> str:
        if self.price == None:
            self.set_price()
        return self.price

    '''-----------------------------------'''

    def get_rank(self) -> str:
        if self.rank == None:
            self.set_rank()
        return self.rank

    '''-----------------------------------'''

    def read_data_wait(self, xpath: str):
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))).text

        return element
    '''-----------------------------------'''

    def read_data(self, xpath: str):
        '''
        :param browser: Selenium browser object.
        :return: None
        '''

        data = self.browser.find_element("xpath", xpath).text
        return data

    '''-----------------------------------'''

    def create_browser(self, url=None):
        '''
        :param url: The website to visit.
        :return: None
        '''
        self.browser = webdriver.Chrome(
            executable_path=chrome_driver, chrome_options=options)
        # Defautl browser route
        if url == None:
            self.browser.get(url=self.hedera_txns_url)
        # External browser route
        else:
            self.browser.get(url=url)

    '''-----------------------------------'''

    def close_browser(self):
        self.browser.close()

    '''-----------------------------------'''

    '''-----------------------------------'''

    def create_screenshot(self) -> None:
        file_name = self.create_image_filename()

        self.browser.get_screenshot_as_file(file_name)

        self.resize_image(file_name=file_name)

        # This is to resize the image to custom dimensions.

    '''-----------------------------------'''

    '''-----------------------------------'''

    def create_image_filename(self) -> str:
        return cwd + "\\Scraper\\Screenshots\\" + "TPS_" + \
            str(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")) + ".png"

    '''-----------------------------------'''

    def resize_image(self, file_name: str):
        # Base image should be 1877 x 1872

        # Create an object for the image file.
        img = Image.open(file_name)
        # Get the dimensions of the image.
        width, height = img.size

        # Adjust how high the crop window is. The higher the number, the higher the window is, vertically.
        height_adjust = 20

        # Size of the window
        vertical_window_size = 10

        left = 300
        top = height / height_adjust
        right = 1572
        bottom = vertical_window_size * height / height_adjust

        img1 = img.crop((left, top, right, bottom))

        img1.save(file_name)

    '''-----------------------------------'''

    def _redirect_browser(self, url: str) -> None:
        self.browser.get(url)
