# pylint: disable=unused-wildcard-import
from helium import *
from selenium.webdriver.common.by import By
from helper import tik, report, rand_scroll
from models import CourseModel, CouponModel, AccountModel


class NewAccountWorker:
    def __init__(self, driver, account):
        self.driver = driver
        self.account = account
        helium.set_driver(self.driver)

    #@report('REGISTERING ACCOUNT')
    def new_account(self):
        self.driver.get('https://www.udemy.com/?persist_locale=&locale=en_US')
        tik().s
        click('Sign up')
        tik().m
        click(S('#id_fullname'))
        tik().s
        write(self.account.name)
        tik().s
        click(S('#email--1'))
        tik().m
        write(self.account.email)
        tik().m
        click(S('#password'))
        tik().s
        write(self.account.pwd)
        tik().s
        click(S('#submit-id-submit'))
        tik().l
        if Button('Skip for now').exists:
            click('Skip for now')
            tik().m
        if not 'join/signup-popup/' in self.driver.current_url:
            return True
        return False

    #@report('SETTING PROFILE ACCOUNT')
    def set_profile(self):
        self.driver.tab_new('https://www.udemy.com/user/edit-profile/')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        tik().l
        write(self.account.quote, into=TextField(above=Text(
            text='Links and coupon codes are not permitted in this section.')))
        tik().m
        scroll_down(rand_scroll(3))
        tik().s
        scroll_down(rand_scroll(3))
        tik().s
        scroll_down(rand_scroll(3))
        tik().s
        click(S('#submit-id-submit'))
        tik().l
        self.driver.get('https://www.udemy.com/user/' +
                         self.account.name.replace(' ', '-').lower() + '/')
        tik().m
        if Text(text=self.account.name).exists:
            return True
        return False

    #@report('CONFIRMING ACCOUNT', tries=2)
    def new_email(self):
        self.driver.tab_new('https://www.guerrillamail.com/inbox')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        tik().l
        click(S('#forget_button'))
        # click('Forget Me')
        tik().l
        select(ComboBox("sharklasers.com"), self.account.email.split('@')[1])
        tik().m
        click(S('#inbox-id'))
        tik().m
        write(self.account.user)
        tik().m
        click('Set')
        tik().l
        if S('#inbox-id').web_element.text != self.account.user:
            self.driver.refresh()
            tik().m
            self.new_email()
        tik().x
        wait_until(Text(text='no-reply@e.udemymail.com').exists,
                   interval_secs=1, timeout_secs=900)
        click(Text(text='no-reply@e.udemymail.com'))
        tik().x
        scroll_down(rand_scroll(3))
        tik().s
        scroll_down(rand_scroll(3))
        tik().s
        click(Link(text='Yes, please'))
        tik().l
        if Link(text='My learning').exists:
            return True
        return False

    # def perform(self):
    #     if self.new_account():
    #         if self.new_email():
    #             if self.set_profile():
    #                 return True
    #     return False
    def perform(self):
        if self.new_account():
            # if self.new_email():
            if self.set_profile():
                return True
        return False


class JoinWorker:
    def __init__(self, driver, account):
        self.driver = driver
        self.account = account
        helium.set_driver(self.driver)

    #@report('CHECKING IF IS LOGGED IN')
    def _is_loggedin(self):
        if self.driver.current_url == 'https://www.udemy.com/user/edit-profile/': return True
        self.driver.get('https://www.udemy.com/user/edit-profile/')
        tik().m
        if not 'join/login-popup/' in self.driver.current_url:
            return True
        return False

    #@report('SIGN IN ACCOUNT')
    def login(self):
        if self._is_loggedin(): return True
        tik().m
        click(S('#submit-id-submit'))
        tik().m
        write(self.account.pwd, into=TextField(label='Password'))
        tik().m
        click(S('#submit-id-submit'))
        tik().m
        return self._is_loggedin()

    #@report('SIGN OUT ACCOUNT')
    def logout(self):
        if not self._is_loggedin(): return True
        tik().l
        logout_link = self.driver.find_element(By.XPATH, '//a[contains(@href,"/user/logout/")]').get_attribute('href')
        tik().s
        self.driver.get(logout_link)
        tik().m
        return self._is_loggedin()

class EnrollWorker:
    def __init__(self, driver, account):
        self.driver = driver
        self.account = account
        helium.set_driver(self.driver)

    def _get_coupons(self, course: CourseModel):
        return [coupon for coupon in course.coupons if coupon.is_valid]

    def checkout(self):
        tik().s
        if Text(text='Your cart is free!').exists and Button(text='Enroll now').exists:
            click(Button(text='Enroll now'))
            tik().l
            if 'cart/success/' in self.driver.current_url:
                return True
        return False
        
    def enroll(self, coupon: CouponModel):
        try:
            self.driver.get(coupon.coupon_url)
        except Exception:
            return False

        tik().l
        scroll_down(rand_scroll(2))
        tik().s
        scroll_up(rand_scroll(1))
        tik().s

        if not coupon.coupon_key in self.driver.current_url:
            return False

        if Button(text='Enroll now').exists:
            try:
                click(Button(text='Enroll now'))
                tik().l
            except Exception:
                return False
            else:
                if self.checkout():
                    return True
        return False
