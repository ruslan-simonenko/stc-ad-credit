from datetime import datetime, date
from typing import List

from sqlalchemy import select

from src.persistence.schema import db
from src.persistence.schema.carbon_audit import CarbonAudit


class CarbonAuditService:
    @staticmethod
    def add(business_id: int, score: int, report_date: date, report_url: str, creator_id: int) -> CarbonAudit:
        carbon_audit = CarbonAudit(
            business_id=business_id,
            score=score,
            report_date=report_date,
            report_url=report_url,
            created_by=creator_id,
            created_at=datetime.utcnow()
        )
        db.session.add(carbon_audit)
        db.session.commit()
        return carbon_audit

    @staticmethod
    def get_all() -> List[CarbonAudit]:
        query = select(CarbonAudit).order_by(CarbonAudit.created_at.desc())
        return db.session.execute(query).scalars().all()
