from datetime import datetime, date
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.sql.functions import count

from src.persistence.schema import db
from src.persistence.schema.ad_record import AdRecord
from src.utils.clock import Clock


class AdRecordService:

    @staticmethod
    def add(business_id: int, ad_post_url: str, creator_id: int) -> AdRecord:
        ad_record = AdRecord(
            business_id=business_id,
            ad_post_url=ad_post_url,
            created_by=creator_id,
            created_at=Clock.now()
        )
        db.session.add(ad_record)
        db.session.commit()
        return ad_record

    @staticmethod
    def get_all() -> List[AdRecord]:
        query = select(AdRecord).order_by(AdRecord.created_at.desc())
        return db.session.execute(query).scalars().all()

    @staticmethod
    def get_count_for_business_since_date(business_id: int, since: datetime) -> int:
        query = select(count(AdRecord.id)) \
            .where(and_(AdRecord.business_id == business_id,
                        AdRecord.created_at >= since))
        return db.session.execute(query).scalar_one()
