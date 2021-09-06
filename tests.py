from webdriver import PicklebleDriver
from coupon import CouponController
from course import CourseController
from account import AccountController
from models import CategoryCourses as cc, TierAccount, CouponModel

raw_coupons = [
    'https://www.udemy.com/course/modern-javascript-es6-for-react-js/?couponCode=FREEJULY7',
    'https://www.udemy.com/course/affiliate-marketing-supremacy-learn-affiliate-marketing/?couponCode=93E579E71911001BCD96',
    'https://www.udemy.com/course/complete-python-bootcamp-expert-course/?couponCode=9107A723581D323340F3',
    'https://www.udemy.com/course/adobe-illustrator-from-zero-to-beyond/?couponCode=ILLUSTRATOR-2021-07',
    'https://www.udemy.com/course/quickbooks-online-qbo-bookkeeping-with-bank-feeds-2021/?couponCode=A00883DAC8A2FCACA7A5',
    'https://www.udemy.com/course/html-css-certification-course-for-beginners-e/?ranMID=39197&ranEAID=%2F7fFXpljNdk&ranSiteID=_7fFXpljNdk-IBrHb1dRXoJxO9gLxsZFRw&LSNPUBID=%2F7fFXpljNdk&utm_source=aff-campaign&utm_medium=udemyads&couponCode=35074F93A29C201F6FAA',
    'https://www.udemy.com/course/introduction-to-computer-science-with-python/?couponCode=FREE-UPSKILLING',
    ]

pdriver = PicklebleDriver()
acc_controller = AccountController()
coupon_controller = CouponController()
course_controller = CourseController()


# add multiple coupons
driver = pdriver.new_driver()
driver.get('https://www.udemy.com/?persist_locale=&locale=en_US')
for raw_url in raw_coupons:
    coupon_controller.get(driver, raw_url)
pdriver.quit(driver)

# add new premium accounts
for dummy in range(6):
    acc = acc_controller.new()
    acc_opt = pdriver.set_options(acc)
    driver = pdriver.new_driver(acc_opt)
    acc_controller.add(driver, acc)
    acc_controller.set_category(acc, [cc.development, cc.it, cc.office, cc.design])
    acc_controller.set_tier(acc, TierAccount.premium)
    valid_coupons = coupon_controller.get_valid_coupons()
    for coupon in valid_coupons:
        course = course_controller.get(driver, coupon['coupon_url'])
        if course.category in acc.categories:
            acc_controller.enroll(driver, acc, CouponModel(**coupon))
    pdriver.quit(driver)
