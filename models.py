# pylint: disable=no-name-in-module
from pydantic import Field, BaseModel, AnyUrl
from pydantic.dataclasses import dataclass
from typing import Optional, List

class CouponModel(BaseModel):
    updated: str

    course_id: str
    coupon_url: AnyUrl # Full url coupon
    coupon_key: str
    is_valid: bool = False

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CourseModel(BaseModel):
    updated: str

    url: AnyUrl  # Full url course
    course_url: str  # part url course
    course_id: str
    
    category: str
    subcategory: str
    title: str
    description: str
    
    rate: str
    ratings: str
    students: str
    created_by: str
    updated_by: str
    language: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StatusAccount:
    unconfirmed = 'unconfirmed'
    confirmed = 'confirmed'
    selled = 'selled'


class TierAccount:
    free = 'free'  # all avalable curses mixed - max 10 courses - $0,00
    premium = 'premium'  # multiple category curses - $1,00 + $0,10 for course
    special = 'special'  # single category curses - $5,00 + $0,10 for course


class CategoryCourses:
    development = 'Development'
    business = 'Business'
    finance = 'Finance & Accounting'
    it = 'IT & Software'
    office = 'Office Productivity'
    personal = 'Personal Development'
    design = 'Design'
    marketing = 'Marketing'
    lifestyle = 'Lifestyle'
    photo = 'Photography & Video'
    health = 'Health & Fitness'
    music = 'Music'
    teaching = 'Teaching & Academics'


class AccountModel(BaseModel):
    created: str
    updated: str

    name: str
    user: str
    email: str
    pwd: str
    quote: str

    courses: List = list()
    total_value: float = 0.0

    categories: str = []
    tier: str = TierAccount.special
    status: str = StatusAccount.confirmed
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
