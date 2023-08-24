import random
import string

from src.business.business_service import BusinessService
from src.business.business_types import BusinessRegistrationType
from src.persistence.schema.business import Business
from src.persistence.schema.user import User


class BusinessTestUtils:
    @staticmethod
    def add_business(creator: User, name: str = None, registration_type: BusinessRegistrationType = None,
                     registration_number: string = None) -> Business:
        def random_string():
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        return BusinessService.add(
            name=name if name else f'Business {random_string()}',
            registration_type=registration_type if registration_type else random.choice(list(BusinessRegistrationType)),
            registration_number=registration_number if registration_number else random_string(),
            email=f'biz-{random_string()}@gmail.com',
            facebook_url=f'https://facebook.com/business/biz-{random_string()}',
            creator_id=creator.id)
