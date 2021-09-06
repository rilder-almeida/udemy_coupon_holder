import os
import random
import logging
from functools import wraps
from time import sleep, perf_counter
from datetime import datetime

import pyparsing as pparse
import uuid

def url_parser(raw_url):
    protocol = pparse.oneOf('http:// https://', caseless=True)('protocol')
    www = pparse.CaselessLiteral('www.')('www')
    udemy = pparse.CaselessLiteral('udemy.com/')('udemy')
    course = pparse.CaselessLiteral('course/')('course')
    course_url = pparse.Word(pparse.alphanums + "-_")('course_url')
    coupon = pparse.CaselessLiteral('couponCode=')('coupon')
    coupon_key = pparse.Word(pparse.alphanums + "-_")('coupon_key')

    if '/?' in raw_url:
        trash_url = raw_url.split('/?')[1]
        if 'couponCode' in trash_url:
            trash_url = trash_url.split('couponCode')[0]
            url_model = pparse.Optional(protocol) + pparse.Optional(www) + pparse.Optional(udemy) + pparse.Optional(
                course) + course_url + '/?' + trash_url + coupon + coupon_key
        else:
            if trash_url == '':
                trash_url = pparse.Empty()
            url_model = pparse.Optional(protocol) + pparse.Optional(www) + pparse.Optional(udemy) + pparse.Optional(
                course) + course_url + '/?' + trash_url
    else:
        url_model = pparse.Optional(protocol) + pparse.Optional(www) + \
            pparse.Optional(udemy) + pparse.Optional(course) + course_url

    url_parsed = url_model.parseString(raw_url)
    full_url = "".join(map(str, url_parsed))
    url = 'https://www.udemy.com/course/' + url_parsed.course_url

    return {
        'full_url': full_url,
        'url': url,
        'course_url': url_parsed.course_url,
        'coupon_key': url_parsed.coupon_key,
    }

def sanitize_snakelowercase(txt):
    import unidecode
    pre_string = ''.join(filter(str.isalpha, txt)).replace('ç', 'c')
    return unidecode.unidecode(pre_string).lower()

def rand_scroll(n):
    ref = 100*n
    minx = int(ref*random.randint(90, 100)/100)
    maxx = int(ref*random.randint(100, 110)/100)
    return random.randint(minx, maxx)

class tik:
    @property
    def s(self):  # about 1s
        t = random.uniform(random.uniform(1, 2), random.uniform(2, 3))
        # print('[PLEASE WAIT] --- {0:.2f}s'.format(t))
        sleep(t)

    @property
    def m(self):  # about 3s
        t = random.uniform(random.uniform(2, 3), random.uniform(4, 5))
        # print('[PLEASE WAIT] --- {0:.2f}s'.format(t))
        sleep(t)

    @property
    def l(self):  # about 10s
        t = random.uniform(random.uniform(10, 15), random.uniform(15, 20))
        # print('[PLEASE WAIT] --- {0:.2f}s'.format(t))
        sleep(t)

    @property
    def x(self):  # about 30s
        t = random.uniform(random.uniform(15, 20), random.uniform(30, 60))
        # print('[PLEASE WAIT] --- {0:.2f}s'.format(t))
        sleep(t)

    def _(self, min, max):
        t = random.uniform(min, max)
        # print('[PLEASE WAIT] --- {0:.2f}s'.format(t))
        sleep(t)


def report(
    task_name,
    tries=1,
    retry_delay=0,
    exceptions=(Exception),
    raises=True
    ):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print('[' + task_name + '] >>> Start: ' + datetime.now().strftime("%H:%M:%S"))
                start_run = perf_counter()
                for i in range(tries):
                    print('[' + task_name + '] --- Attempting (' + str(i+1) + '/' + str(tries) + ')')
                    start_lap = perf_counter()
                    try:
                        result = func(*args, **kwargs)
                        print('[' + task_name + '] ::: Success')
                        break
                    except exceptions as error:
                        print('[' + task_name + '] ::: Fail')
                        print('\n')
                        logging.basicConfig(level=logging.DEBUG)
                        logger = logging.getLogger(__name__)
                        logger.exception(error)
                        print('\n')
                    finally:
                        stop_lap = perf_counter()
                        lap_time = stop_lap - start_lap
                        print('[' + task_name + f'] --- Attempting duration: {lap_time: 0.4f}s')
                    print('[' + task_name + f'] --- Attempting interval: {retry_delay}s')
                    sleep(retry_delay)
                stop_run = perf_counter()
                print('[' + task_name + '] <<< End ' + datetime.now().strftime("%H:%M:%S"))
                run_time = stop_run - start_run
                print('[' + task_name + f'] --- Task duration: {run_time: 0.4f}s')
                return result
            except UnboundLocalError:
                if not raises:
                    return
                else:
                    raise
        return wrapper
    return decorator

def check_and_create_path(diretory_path):
    if not os.path.isdir(diretory_path):
        os.makedirs(diretory_path)
        sleep(3)
    return diretory_path
