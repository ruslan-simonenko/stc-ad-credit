from datetime import datetime
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.persistence.schema import db
from src.persistence.schema.business import Business
from src.persistence.schema.user import User


class BusinessService:
    @staticmethod
    def add(name: str, facebook_link: Optional[str], creator: User) -> Business:
        business = Business(
            name=name,
            facebook_link=facebook_link,
            created_by=creator.id,
            created_at=datetime.utcnow()
        )
        db.session.add(business)
        try:
            db.session.commit()
        except IntegrityError as e:
            raise ValueError(e, 'Business name is already in use')
        return business

