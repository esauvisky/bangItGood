#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import json
from pprint import pprint
from logzero import logger
from selenium import webdriver
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from tkinter import messagebox

POINTS_MALL_URL = "https://www.banggood.com/pointsmall.html"
BLACK_FRIDAY_URL = "https://www.banggood.com/banggood-black-friday-carve-up-bonuses-2019.html"
LOGIN_PAGE_URL = "https://www.banggood.com/login.html"


def save_login_cookies(username=False, password=False):
    browser = webdriver.Chrome()
    browser.get(LOGIN_PAGE_URL)

    if not (username and password):
        username = 'bogus'
        ## Blocking manual user input:
        messagebox.showinfo(
            title='Manual Login',
            message='Fill entry boxes, 2FA, click submit, wait for loading and click OK.')
    else:
        ## Nonblocking automatic input:
        browser.find_element_by_id('login-email').send_keys(username)
        browser.find_element_by_id('login-pwd').send_keys(password)
        browser.find_element_by_id('login-submit').click()

    ## Writes to file:
    with open('cookies/' + str(username) + '.txt', 'w+') as file:
        file.write(json.dumps(browser.get_cookies()))


def main(args):
    """ Main entry point of the app """
    logger.info(args)

    driver = webdriver.Chrome()

    with open(args.cookies, 'r') as file:
        cookies = json.load(file)

    driver.get(LOGIN_PAGE_URL)

    filtered_cookies = [{ key: value for key, value in c.items() if key in ('name', 'value', 'path', 'domain', 'secure') } for c in cookies]

    for cookie in filtered_cookies:
        driver.add_cookie(cookie)

    pprint(driver.get_cookies())

    driver.get(POINTS_MALL_URL)
    if POINTS_MALL_URL in driver.current_url:
        driver.find_element_by_partial_link_text('CHECK-IN').click()

    # browser.get(BLACK_FRIDAY_URL)
    # for i in fs.
    #  driver.add_cookie({'name': 'foo', 'value': 'bar'})
    # bgTasks = browser.find_elements_by_css_selector('.J-task-btn')
    # for bgTask in bgTasks:
    #     bgTask.click()
    #     if POINTS_MALL_URL in browser.current_url:
    #         browser.find_element('javascript:;')
    #     else:
    #         breakpoint()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    #     # Required single positional argument
    #     parser.add_argument("arg",
    #                         help="Required positional argument (a single thing).")

    #     # Required multime positional arguments
    #     parser.add_argument('items', nargs='+',
    # a                        help='Required various positional arguments (a list).')

    # Optional argument flag which defaults to False
    # parser.add_argument("-c", "--cookies", action="store_true", default=False,
    #                     help="Cookie file to use")
    parser.add_argument("-c", "--cookies", action="store_true", default='./cookies/francosauvisky@gmail.com.txt',
                        help="Cookie file to use")

    #     # Optional argument which requires a parameter (eg. -d test)
    #     parser.add_argument("-n", "--name", action="store", dest="name",
    #                         help="Specifies a name if necessary.")

    #     # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    #     parser.add_argument("-v", "--verbose", action="count", default=0,
    #                         help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version", action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
