import os
import random
import undetected_chromedriver.v2 as uc
import pickle

from repositories import ProxyApi
from helper import tik, check_and_create_path, report

OPTIONS_ARGS = [
    # '--disable-gpu',
    # '--disable-dev-shm-usage',
    # '--ignore-ssl-errors',
    # '--ignore-certificate-errors',
    # '--enable-javascript'
    # "--lang=en-US"
    "--lang=en",
    '--disable-extensions',
    '--no-sandbox',
    '--no-default-browser-check',
    '--no-service-autorun',
    '--no-first-run',
    '--password-store=basic',
    '--disable-notifications',
]

COOKIES_WEBSITES = ["https://www.udemy.com", "https://udemy.com"]

class PicklebleDriver(object):
    def set_options(self, account=None, arguments: list = OPTIONS_ARGS, proxy: bool = False):
        options = uc.ChromeOptions()
        # Grants a unique profile data files for chromium or uses a temp profile
        session_path = check_and_create_path(
            './sessions/temp') if account is None else check_and_create_path(
                './sessions/' + account.user)
        arguments.append("--user-data-dir="+session_path)
        for arg in arguments:
            options.add_argument(arg)
        if proxy:
            proxy_list = ProxyApi().get(5)
            options.add_argument(
                '--proxy-server={}'.format(random.sample(proxy_list, 1)[0]))
        return options

    def new_driver(self, options=None, headless: bool = False):
        try:
            options = self.set_options() if options is None else options
            driver = uc.Chrome(options=options, headless=headless)
            driver.implicitly_wait(15)
            driver.set_page_load_timeout(90)
            driver.set_script_timeout(90)
            driver.maximize_window()
            tik().s
            return driver
        except Exception:
            # FIXME Infinite Try
            self.new_driver(options)

    def load_driver(self, account, options=None, cookies_websites=COOKIES_WEBSITES):
        try:
            session_path = check_and_create_path(
                './sessions/temp') if account is None else check_and_create_path(
                './sessions/' + account.user)
            options = self.set_options(account=account) if options is None else options
            driver = self.new_driver(options=options)
            with open(session_path + '/cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)
            for website in cookies_websites:
                driver.get(website)
                tik().m
                for cookie in cookies:
                    expiry = cookie.get('expiry', None)
                    if expiry:
                        cookie['expiry'] = int(expiry * 1000)
                    driver.add_cookie(cookie)
                tik().m
                driver.refresh()
        except FileNotFoundError:
            # FIXME Ignore Error
            pass

    def save_driver(self, driver, account=None):
        cookies = driver.get_cookies()
        session_path = check_and_create_path(
            './sessions/temp') if account is None else check_and_create_path(
            './sessions/' + account.user)
        with open(session_path + '/cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file, protocol=pickle.HIGHEST_PROTOCOL)

    def new_tab(self, driver, url='about:blank'):
        driver.tab_new(url)
        driver.switch_to.window(driver.window_handles[-1])

    def all_tabs(self, driver):
        _report = {driver.session_id: {'tabs': {}}}
        tabs = driver.window_handles
        for tab in tabs:
            driver.switch_to.window(tab)
            _report[driver.session_id]['tabs'].update(
                {
                    driver.current_window_handle: {
                        'url': driver.current_url,
                        'title': driver.title
                    }
                })
        driver.switch_to.window(driver.window_handles[0])
        return _report

    def get_tab(self, driver, tab):
        try:
            return driver.switch_to.window(tab)
        except Exception:
            tab_list = self.all_tabs(driver)[driver.session_id]['tabs']
            for handle in list(tab_list.keys()):
                if (tab_list[handle] == tab or
                    tab_list[handle]['url'] in tab or
                    tab in tab_list[handle]['url'] or
                    tab_list[handle]['title'] in tab or
                        tab in tab_list[handle]['title']):
                    return driver.switch_to.window(handle)

    def close_tab(self, driver, tab):
        current_tab = driver.current_window_handle
        self.get_tab(driver, tab)
        driver.execute_script('window.close()')
        driver.switch_to.window(current_tab)

    def close_all_tabs(self, driver):
        if len(driver.window_handles) < 1:
            return
        for window_handle in driver.window_handles[:]:
            driver.switch_to.window(window_handle)
            driver.close()

    def quit(self, driver, account=None):
        self.save_driver(driver, account)
        self.close_all_tabs(driver)
        driver.quit()
