from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Event
from schemas.event import AddEventDB, DeleteEventDB, EditEventDB, EventDB

router = APIRouter(prefix='/event')


@router.get('/get_events',
            response_model=list[EventDB],
            summary="Get Events",
            description="Get Events from database")
async def get_events(skip: Annotated[int, Query(description='Pagination skip size', ge=1)] = 0,
                     limit: Annotated[int, Query(description='Pagination page size', ge=1)] = 10, 
                     db: AsyncSession = Depends(get_db)):
    query = select(Event).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_event',
             response_model=EventDB,
             summary="Add Event",
             description="Add Event to database")
async def add_event(*, request: Request, form: AddEventDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Event).values(*form.dict()).returning(Event)
    ev = await db.execute(stmt)
    return ev


@router.post('/update_event',
             response_model=EventDB,
             summary="Update Event",
             description="Update Event in database")
async def update_event(*, request: Request, form: EditEventDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_event']
    stmt = (update(Event)
            .values(*v)
            .where(Event.id_event == form.id_event)
            .returning(Event))
    ev = await db.execute(stmt)
    return ev


@router.post('/delete_event',
             summary="Delete Event",
             description="Delete Event from database")
async def delete_event(*, request: Request, form: DeleteEventDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(EventDB)
        .where(Event.id_event == form.id_event)
    )
    await db.execute(stmt)
