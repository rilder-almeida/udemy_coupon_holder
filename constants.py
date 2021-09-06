from tinydb import TinyDB, Query

from helper import check_and_create_path

PROXY_JUDGES = [
    'http://httpbin.org/get?show_env',
    'https://httpbin.org/get?show_env',
    'https://www.udemy.com/join/signup-popup',
    'https://www.guerrillamail.com/inbox',
]

PROXY_PROVIDERS = None  # []

PROXY_TYPES = [('HTTP', ('Anonymous', 'High')),
               ('HTTPS', ('Anonymous', 'High'))]

PROXY_COUNTRIES = ['BR']

GUERRILLA_DOMAINS = [
    "sharklasers.com",
    "guerrillamail.info",
    "grr.la",
    "guerrillamail.biz",
    "guerrillamail.com",
    "guerrillamail.de",
    "guerrillamail.net",
    "guerrillamail.org",
    "guerrillamailblock.com",
    "pokemail.net",
    "spam4.me"]

DATA_PATH = check_and_create_path('./data/')

DATA_FILE_ACCOUNT = 'account.json'
DB_ACCOUNT = TinyDB(DATA_PATH + DATA_FILE_ACCOUNT)

DATA_FILE_COURSE = 'course.json'
DB_COURSE = TinyDB(DATA_PATH + DATA_FILE_COURSE)

DATA_FILE_COUPON = 'coupon.json'
DB_COUPON = TinyDB(DATA_PATH + DATA_FILE_COUPON)

where = Query()

account_table = DB_ACCOUNT.table('account_table')
course_table = DB_COURSE.table('course_table')
coupon_table = DB_COUPON.table('coupon_table')
