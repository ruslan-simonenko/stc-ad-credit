import random
import string

from src.business.business_service import BusinessService
from src.persistence.schema.business import Business
from src.persistence.schema.user import User


class BusinessTestUtils:
    @staticmethod
    def add_business(creator: User, name: str = None) -> Business:
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        return BusinessService.add(
            name=name if name else f'Business {random_string}',
            facebook_url=f'https://facebook.com/business/biz-{random_string}',
            creator_id=creator.id)