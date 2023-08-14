from datetime import datetime, date
from typing import List, Dict

from sqlalchemy import select, and_, join
from sqlalchemy.sql.functions import count

from src.persistence.schema import db
from src.persistence.schema.ad_record import AdRecord
from src.persistence.schema.business import Business
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

    @staticmethod
    def get_count_for_all_businesses_since_date(since: datetime) -> Dict[int, int]:
        join_ = join(Business, AdRecord,
                     onclause=and_(
                         Business.id == AdRecord.business_id,
                         AdRecord.created_at >= since),
                     isouter=True)
        query = select(Business.id, count(AdRecord.id)) \
            .select_from(join_) \
            .group_by(Business.id)

        result = db.session.execute(query).all()
        return {business_id: num_records for business_id, num_records in result}
