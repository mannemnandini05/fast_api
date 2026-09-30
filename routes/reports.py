from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import services


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/revenue")
def revenue_report(
    doctor_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=400,
            detail="from_date cannot be greater than to_date",
        )

    report = services.get_revenue_report(
        db,
        doctor_id,
        from_date,
        to_date,
    )

    return {
        "doctor_id": doctor_id,
        "from_date": from_date,
        "to_date": to_date,
        "data": [
            {
                "doctor_id": row.doctor_id,
                "total_revenue": row.total_revenue or 0,
            }
            for row in report
        ],
    }