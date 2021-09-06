from datetime import datetime

from constants import where
from database import CourseDB
from helper import url_parser
from models import CourseModel
from scraper import Scraper

class CourseController:  
    def scrap(self, driver, raw_url):
        processed_url = url_parser(raw_url)
        scraper = Scraper(driver, processed_url)
        try:
            course_scraped = scraper.get_course()
            course_scraped.update({'updated': str(datetime.now())})
        except Exception:
            raise Exception('Não conseguiu scrapar o curso')
            # return None
        else:
            return CourseModel(**course_scraped)
    
    def get(self, driver, raw_url):
        processed_url = url_parser(raw_url)
        course = CourseDB().get( cond = where.course_url == processed_url['course_url'])
        if course is None:
            course = self.scrap(driver, raw_url)
            CourseDB().upsert(course)
        return course

    def fix_up(self, driver, course: CourseModel):  # verify course, if necessary scrap again
        ...
