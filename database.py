from datetime import datetime

from helper import report
from models import AccountModel, CourseModel, CouponModel
from constants import (
    account_table,
    course_table,
    coupon_table,
    where,
)

class AccountDB:

    def get(self, cond=None, doc_id: int = None):
        account = account_table.get(cond=cond, doc_id=doc_id)
        return CourseModel(**account) if account is not None else None

    def get_all(self):
        return [AccountModel(**account_table_doc) for account_table_doc in account_table.all()]

    def search(self, cond):
        return account_table.search(cond)

    def insert(self, account: AccountModel):
        account.updated = str(datetime.now())
        account_table.insert(account.dict())

    def delete(self, account: AccountModel):
        account_table.remove(where.user == account.user)
    
    def update(self, account: AccountModel):
        account.updated = str(datetime.now())
        account_table.update(account.dict(), where.user == account.user)

    def upsert(self, account: AccountModel):
        account.updated = str(datetime.now())
        account_table.upsert(account.dict(), where.user == account.user)


class CourseDB:
    def get(self, cond=None, doc_id: int = None):
        course = course_table.get(cond=cond, doc_id=doc_id)
        return CourseModel(**course) if course is not None else None

    def get_all(self):
        return [CourseModel(**course_table_doc) for course_table_doc in course_table.all()]

    def search(self, cond):
        return course_table.search(cond)

    def insert(self, course: CourseModel):
        course.updated = str(datetime.now())
        course_table.insert(course.dict())

    def delete(self, course: CourseModel):
        course_table.remove(where.course_id == course.course_id)

    def update(self, course: CourseModel):
        course.updated = str(datetime.now())
        course_table.update(course.dict(), where.course_id == course.course_id)
    
    def upsert(self, course: CourseModel):
        course.updated = str(datetime.now())
        course_table.upsert(course.dict(), where.course_id == course.course_id)


class CouponDB:
    def get(self, cond=None, doc_id: int = None):
        coupon = coupon_table.get(cond=cond, doc_id=doc_id)
        return CouponModel(**coupon) if coupon is not None else None

    def get_all(self):
        return [CouponModel(**coupon_table_doc) for coupon_table_doc in coupon_table.all()]

    def search(self, cond):
        return coupon_table.search(cond)

    def insert(self, coupon: CouponModel):
        coupon.updated = str(datetime.now())
        coupon_table.insert(coupon.dict())

    def delete(self, coupon: CouponModel):
        coupon_table.remove(where.coupon_url == coupon.coupon_url)

    def update(self, coupon: CouponModel):
        coupon.updated = str(datetime.now())
        coupon_table.update(coupon.dict(), where.coupon_url == coupon.coupon_url)
    
    def upsert(self, coupon: CouponModel):
        coupon.updated = str(datetime.now())
        coupon_table.upsert(coupon.dict(), where.coupon_url == coupon.coupon_url)
