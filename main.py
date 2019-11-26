#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import json
import re
from tkinter import messagebox

import logzero
from logzero import logger
from selenium import common, webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

POINTS_MALL_URL = "https://www.banggood.com/pointsmall.html"
BLACK_FRIDAY_URL = "https://www.banggood.com/banggood-black-friday-carve-up-bonuses-2019.html"
LOGIN_PAGE_URL = "https://www.banggood.com/login.html"


def save_login_cookies(username=False, password=False):
    browser = webdriver.Chrome()
    browser.get(LOGIN_PAGE_URL)

    if not password:
        ## Blocking manual user input:
        browser.find_element_by_id('login-email').send_keys(username)
        messagebox.showinfo(
            title='Manual Login',
            message='Fill entry boxes, 2FA, click submit, wait for loading and click OK.')
    else:
        ## Nonblocking automatic input:
        browser.find_element_by_id('login-email').send_keys(username)
        browser.find_element_by_id('login-pwd').send_keys(password)
        browser.find_element_by_id('login-submit').click()

    ## Writes to file:
    filename = 'cookies/' + str(username) + '.txt'
    with open(filename, 'w+') as file:
        file.write(json.dumps(browser.get_cookies()))

    return filename


def main(args):
    """ Main entry point of the app """
    logger.setLevel(args.verbose)

    logger.debug(args)

    if args.username:
        filename = save_login_cookies(username=args.username)
        logger.info('Saved cookies at %s', filename)
        return (0)

    for cookiefile in args.cookies:
        # Headless mode if --quiet
        options = webdriver.ChromeOptions()
        if args.quiet:
            options.add_argument('headless')

        driver = webdriver.Chrome(options=options)

        with open(cookiefile, 'r') as file:
            cookies = json.load(file)

        filtered_cookies = [{
            key: value
            for key, value in c.items()
            if key in ('name', 'value', 'path', 'domain', 'secure')}
                            # if key in ('name', 'value', 'path', 'secure')}
                            for c in cookies]

        # Waits at most 15 seconds per page load
        # (sometimes it hangs up)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        ## Alternative: https://intellipaat.com/community/10338/how-do-i-set-the-selenium-webdriver-get-timeout
        # WebDriverWait(driver,)

        try:
            # Must open any page once before adding cookies
            logger.info('Opening %s', LOGIN_PAGE_URL)
            driver.get(LOGIN_PAGE_URL)
        except:
            logger.error('Got stuck at %s. Continuing...', LOGIN_PAGE_URL)
            driver.execute_script("window.stop();")

        # Adds cookies
        try:
            username = re.match(r'^.+/(.+)\.', cookiefile)[1]
        except:
            username = str(cookiefile)

        logger.warning('Adding cookies for user %s', username)
        for cookie in filtered_cookies:
            logger.debug('Adding cookie: %s', cookie['name'])
            driver.add_cookie(cookie)
        # pprint(driver.get_cookies())

        # Opens page and clicks button
        try:
            logger.info('Opening %s', POINTS_MALL_URL)
            driver.get(POINTS_MALL_URL)
        except:
            logger.error('Got stuck at %s. Continuing...', POINTS_MALL_URL)
            driver.execute_script("window.stop();")

        try:
            logger.info('Clicking CHECK-IN button.')
            driver.find_element_by_partial_link_text('CHECK-IN').click()
        except common.exceptions.NoSuchElementException:
            logger.error("Couldn't find CHECK-IN button. Moving on...")
        else:
            logger.warning('Clicked button! Moving on...')
        finally:
            driver.quit()

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

    parser.add_argument(
        "-l", "--learn", action="store", dest="username",
        help="Learn mode to grab cookies for one particular username")

    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Uses headless mode and does not open the chrome UI.")

    parser.add_argument('cookies', nargs='+', help="List of cookie files to use in JSON format.")

    parser.add_argument(
        "-v", "--verbose", action="count", default=1, help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version", action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    logzero.loglevel(logzero.logging.INFO)
    args = parser.parse_args()
    main(args)
