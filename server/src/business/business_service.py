from datetime import datetime
from typing import Optional, List

from sqlalchemy import select

from src.business.business_types import BusinessRegistrationType
from src.persistence.schema import db
from src.persistence.schema.business import Business


class BusinessService:
    @staticmethod
    def add(name: str,
            registration_type: BusinessRegistrationType,
            registration_number: str,
            email: Optional[str],
            facebook_url: Optional[str],
            creator_id: int) -> Business:
        with db.session.begin_nested():
            business = Business(
                name=name,
                registration_type=registration_type.value,
                registration_number=registration_number,
                email=email,
                facebook_url=facebook_url,
                created_by=creator_id,
                created_at=datetime.utcnow()
            )
            db.session.add(business)
        return business

    @staticmethod
    def update(business_id: int,
               name: Optional[str] = None,
               registration_type: Optional[BusinessRegistrationType] = None,
               registration_number: Optional[str] = None,
               email: Optional[str] = None,
               facebook_url: Optional[str] = None):
        with db.session.begin_nested():
            business = BusinessService.get_by_id_or_throw(business_id)
            if name is not None:
                business.name = name
            if registration_type is not None:
                business.registration_type = registration_type
            if registration_number is not None:
                business.registration_number = registration_number
            if email is not None:
                business.email = email
            if facebook_url is not None:
                business.facebook_url = facebook_url
        db.session.refresh(business)
        return business

    @staticmethod
    def get_all() -> List[Business]:
        return db.session.execute(select(Business)).scalars().all()

    @staticmethod
    def get_by_id_or_throw(business_id: int) -> Business:
        return db.session.execute(select(Business).where(Business.id == business_id)).scalars().one()
