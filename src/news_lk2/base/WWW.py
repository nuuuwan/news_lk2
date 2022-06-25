"""Utils for reading remote files."""
import ssl

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) '
    + 'Gecko/20100101 Firefox/65.0'
)
ENCODING = 'utf-8'
SELENIUM_SCROLL_REPEATS = 3
SELENIUM_SCROLL_WAIT_TIME = 0.5

# pylint: disable=W0212
ssl._create_default_https_context = ssl._create_unverified_context


class WWW:
    def __init__(self, url):
        self.url = url

    def readBinary(self):
        try:
            resp = requests.get(self.url, headers={'user-agent': USER_AGENT})
            if resp.status_code != 200:
                return None
            return resp.content
        except requests.exceptions.ConnectionError:
            return None

    def read(self):
        binary = self.readBinary()
        if not binary:
            return None
        return binary.decode()

    def readSelenium(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        content = driver.page_source
        driver.quit()
        return content
