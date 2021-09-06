from datetime import datetime

from constants import where
from course import CourseController
from database import CouponDB
from helper import url_parser
from models import CouponModel
from scraper import Scraper

class CouponController:
    def scrap(self, driver, raw_url, course_id):
        processed_url = url_parser(raw_url)
        scraper = Scraper(driver, processed_url)
        try:
            coupon_scraped = scraper.get_coupon()
            coupon_scraped.update({'updated': str(datetime.now())})
            coupon_scraped.update({'course_id': course_id})
        except Exception:
            raise Exception('Não conseguiu scrapar o cupon')
            # return None
        else:
            return CouponModel(**coupon_scraped)

    def get(self, driver, raw_url):
        processed_url = url_parser(raw_url)
        course = CourseController().get(driver, raw_url)
        coupons = CouponDB().search(where.course_id == course.course_id)
        for coupon in coupons:
            if coupon['coupon_key'] == processed_url['coupon_key']:
                if coupon['is_valid']:
                    return CouponModel(**coupon)
        coupon = self.scrap(driver, raw_url, course.course_id)
        CouponDB().upsert(coupon)
        return coupon

    def get_valid_coupons(self):
        return CouponDB().search(where.is_valid == True)
           
    def invalidate(self, coupon: CouponModel):
        ...
    
    def fix_up(self): #verify coupon, delete non valid
        ...
