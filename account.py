from datetime import datetime
import random
import uuid

from constants import GUERRILLA_DOMAINS
from database import AccountDB
from helper import sanitize_snakelowercase
from models import AccountModel, CouponModel, StatusAccount, TierAccount, CategoryCourses
from repositories import NameApi, MussumApi
from workers import NewAccountWorker, JoinWorker, EnrollWorker

class AccountController:
    def _new_name(self) -> list:
        adj = [' de ', ' e ', ' ']
        raw_name = NameApi().new()
        return [
            raw_name[0],
            ' ',
            raw_name[1],
            adj[random.randint(0, 2)],
            raw_name[2]
        ]

    def _new_user(self, name) -> list:
        return [
            sanitize_snakelowercase(name[0]),
            uuid.uuid4().hex[:2],
            '.',
            sanitize_snakelowercase(name[2]),
            '{}'.format(random.randint(72, 99)),
        ]

    def _new_email(self, user) -> list:
        domain = GUERRILLA_DOMAINS[random.randint(0, 10)]
        return [user, '@', domain]

    def _new_pwd(self):
        return uuid.uuid4().hex[:12]

    def _new_quote(self):
        return MussumApi().quote()

    def new(self):
        name = self._new_name()
        user = "".join(map(str, self._new_user(name)))
        email = "".join(map(str, self._new_email(user)))
        pwd = self._new_pwd()
        quote = self._new_quote()
        return AccountModel(
            created=str(datetime.now()),
            updated=str(datetime.now()),
            name="".join(map(str, name)),
            user=user,
            email=email,
            pwd=pwd,
            quote=quote,
        )

    def login(self, driver, account: AccountModel):
        return JoinWorker(driver, account).login()

    def logout(self, driver, account: AccountModel):
        return JoinWorker(driver, account).logout()

    def add(self, driver, account: AccountModel = None):
        acc = self.new() if account is None else account
        if NewAccountWorker(driver, acc).perform():
                AccountDB().upsert(acc)
        else:
            acc = account
            if NewAccountWorker(driver, acc).perform():
                AccountDB().upsert(acc)

    def enroll(self, driver, account: AccountModel, coupon: CouponModel):
        if not coupon.course_id in account.courses:
            if EnrollWorker(driver = driver, account = account).enroll(coupon = coupon):
                account.courses.append(coupon.course_id)
                AccountDB().upsert(account)
            
    def set_category(self, account, categories):
        account.categories = categories
        AccountDB().upsert(account)

    def set_tier(self, account, tier: TierAccount):
        account.tier = tier
        AccountDB().upsert(account)

    def set_status(self, account, status: StatusAccount):
        account.status = status
        AccountDB().upsert(account)

    def fix_up(self):  # verify account, delete if necessary acconts
        ...
