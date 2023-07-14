from datetime import datetime
from typing import Annotated

from db.database import get_db
from fastapi import APIRouter, Depends, Query
from models.models import Notification
from schemas.notification import (AddNotificationDB, DeleteNotificationDB,
                                  EditNotificationDB, NotificationDB,
                                  UpdateDataNotificationDB)
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

router = APIRouter(prefix='/notification')


@router.get('/get_notifications',
            response_model=list[NotificationDB],
            summary="Get Notification",
            description="Get list of Notifications")
async def get_notifications(skip: Annotated[int, Query(description='Pagination skip size', ge=1)] = 0,
                            limit: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
                            db: AsyncSession = Depends(get_db)):
    query = select(Notification).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_notification',
             response_model=NotificationDB,
             summary="Add Notification",
             description="Add Notification to database")
async def add_notification(*, request: Request, form: AddNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Notification).values(*form.dict()).returning(Notification)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/update_notification',
             response_model=NotificationDB,
             summary="Update Notification",
             description="Update Notification in database")
async def update_notification(*, request: Request, form: EditNotificationDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_notification']
    stmt = (update(Notification)
            .values(*v)
            .where(Notification.id_notification == form.id_notification)
            .returning(Notification))
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_notification',
             summary="Delete Notification",
             description="Delete Notification from database")
async def delete_notification(*, request: Request, form: DeleteNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(NotificationDB)
        .where(Notification.id_notification == form.id_notification)
    )
    await db.execute(stmt)


@router.post('/update_data_notification',
             summary="Update Data Notifications",
             description="Set last update date for content in notifications")
async def update_data_notification(*, request: Request, form: UpdateDataNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = (update(Notification)
            .values(last_update=datetime.now())
            .where(Notification.id_content == form.id_content))
    await db.execute(stmt)
