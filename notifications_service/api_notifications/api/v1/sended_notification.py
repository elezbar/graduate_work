from datetime import datetime

from db.database import get_db
from fastapi import APIRouter, Depends
from schemas.sended_notification import DeleteSendedNotification
from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import SendedNotification
from schemas.sended_notification import (
    AddSendedNotification, CheckSendedNotification, SendedNotificationDB)

router = APIRouter(prefix='/sended_notification')


@router.post('/add_sended_notification',
             summary="Add sended notification",
             description="Add a new sended notification to database")
async def add_sended_notification(*, form: AddSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = insert(SendedNotification).values(*form.dict()).returning(SendedNotification)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_sended_notification',
             response_model=SendedNotificationDB,
             summary="Delete sended notification",
             description="Delete sended notification from database")
async def delete_sended_notification(*, form: DeleteSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(SendedNotification)
        .where(SendedNotification.id_sended_notification == form.id_sended_notification)
    )
    await db.execute(stmt)


@router.post('/check_sended_notification',
             summary="Check sednded notification",
             description="Sets the date on which the recipient checks the notification")
async def check_sended_notification(*, form: CheckSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = (update(SendedNotification)
            .values(date_check=datetime.now())
            .where(SendedNotification.id_sended_notification == form.id_sended_notification))
    await db.execute(stmt)
