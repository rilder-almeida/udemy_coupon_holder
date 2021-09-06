# pylint: disable=unused-wildcard-import
from helium import *
from helper import tik, report, rand_scroll

UDEMY_ELEMENTS = {
    'course_page':{
        'category_field': '#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div.course-landing-page__main-content.course-landing-page__topic-menu.dark-background-inner-text-container > div > div',
        'title_field': '#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div:nth-child(4) > div > div.udlite-text-sm.clp-lead > div.clp-component-render > h1',
        'description_field': '#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div:nth-child(4) > div > div.udlite-text-sm.clp-lead > div.clp-component-render > div',
        'stars_field': '#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div:nth-child(4) > div > div.udlite-text-sm.clp-lead > div.clp-lead__badge-ratings-enrollment > div > div:nth-child(1) > div > div > div > span > span.udlite-heading-sm.star-rating--rating-number--3lVe8',
        'price_field': '#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background > div > div > div.course-landing-page__main-content.course-landing-page__purchase-section__main.dark-background-inner-text-container > div > div > div > div > div.generic-purchase-section--buy-box-main--siIXV > div > div'
    }
}

class Scraper:

    def __init__(self, driver, processed_url):
        self.driver = driver
        self.processed_url = processed_url
        helium.set_driver(self.driver)

    #@report('GETTING COURSE ID')
    def _get_course_id(self):
        try:
            tik().s
            scroll_down(rand_scroll(4))
            tik().s
            click('Buy now')
        except Exception:
            raise Exception('Não achou botão comprar')
            # return None
        else:
            tik().m
            head_url = 'https://www.udemy.com/join/signup-popup/?next=%2Fcart%2Fcheckout%2Fexpress%2Fcourse%2F'
            return self.driver.current_url.replace(head_url,'').split('%2F%3F')[0]

    def get_course(self):
        try:
            self.driver.get(self.processed_url['url'])
        except Exception:
            raise Exception('Não achou o site')
            # return None
        tik().m
        
        result = S('#br > div.main-content-wrapper > div.main-content > div.paid-course-landing-page__container > div.top-container.dark-background').web_element.text.split('\n')

        url = self.processed_url['url']
        course_url = self.processed_url['course_url']
        category = result[0]
        subcategory = result[1]
        
        pre_index = 0
        for part in result:
            if part.startswith('Rating:'):
                clas_index = result.index(part)
            if part.startswith('Preview'):
                pre_index = result.index(part)

        if pre_index != 0:
            title = result[pre_index + 1]
            description = result[pre_index + 2]
        else:
            title = S(UDEMY_ELEMENTS['course_page']['title_field']).web_element.text
            description = S(UDEMY_ELEMENTS['course_page']['description_field']).web_element.text

        rate = result[clas_index + 1]
        ratings = result[clas_index + 2]
        students = result[clas_index + 3]
        created_by = result[clas_index + 4]
        updated_by = result[clas_index + 5]
        language = result[clas_index + 6]
        
        tik().s

        course_id = self._get_course_id()

        return {
                'url': url,
                'course_url': course_url,
                'course_id': course_id,

                'category': category,
                'subcategory': subcategory,
                'title': title,
                'description': description,

                'rate': rate,
                'ratings': ratings,
                'students': students,
                'created_by': created_by,
                'updated_by': updated_by,
                'language': language,
            }

    def get_coupon(self):
        coupon_url = self.processed_url['url'] + '/?couponCode=' + self.processed_url['coupon_key']
        try:
            if coupon_url != self.driver.current_url: self.driver.get(coupon_url)
        except Exception:
            raise Exception('Não achou o site')
            # return None
        else:
            tik().l

        if not '/?couponCode=' in self.driver.current_url:
            return {
                'coupon_url': coupon_url,
                'coupon_key': self.processed_url['coupon_key'],
                'is_valid': False
                }

        if Button(text='Enroll now').exists:
            return {
                'coupon_url': coupon_url,
                'coupon_key': self.processed_url['coupon_key'],
                'is_valid': True
                }

        return {
            'coupon_url': coupon_url,
            'coupon_key': self.processed_url['coupon_key'],
            'is_valid': False
            }
