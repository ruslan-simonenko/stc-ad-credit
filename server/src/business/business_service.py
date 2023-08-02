from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.persistence.schema import db
from src.persistence.schema.business import Business


class BusinessService:
    @staticmethod
    def add(name: str, facebook_url: Optional[str], creator_id: int) -> Business:
        business = Business(
            name=name,
            facebook_url=facebook_url,
            created_by=creator_id,
            created_at=datetime.utcnow()
        )
        db.session.add(business)
        try:
            db.session.commit()
        except IntegrityError as e:
            raise ValueError(e, 'Business name is already in use')
        return business

    @staticmethod
    def get_all() -> List[Business]:
        return db.session.execute(select(Business)).scalars().all()
