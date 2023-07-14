from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Unsubscribe
from schemas.unsubscribe import (AddUnsubscribeDB, RemoveUnsubscribeDB,
                                 UnsubscribeDB, EditUnsubscribeDB)

router = APIRouter(prefix='/unsubscribe')


@router.get('/get_unsubscribes',
            response_model=list[UnsubscribeDB],
            summary="get unsubscribes",
            description="Get unsubscribes from database")
async def get_UnsubscribeDBs(skip: Annotated[int, Query(description='Pagination skip size', ge=1)] = 0,
                             limit: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
                             db: AsyncSession = Depends(get_db)):
    query = select(Unsubscribe).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_unsubscribe',
             response_model=UnsubscribeDB,
             summary="Add unsubscribe",
             description="Add unsubscribe to database")
async def add_unsubscribe(*, request: Request, form: AddUnsubscribeDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Unsubscribe).values(*form).returning(Unsubscribe)
    unsub = await db.execute(stmt)
    return unsub


@router.post('/update_unsubscribe',
             response_model=UnsubscribeDB,
             summary="Update unsubscribe",
             description="Update unsubscribe in database")
async def update_unsubscribe(*, request: Request, form: EditUnsubscribeDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_unsubscribe']
    stmt = (update(Unsubscribe)
            .values(*v)
            .where(Unsubscribe.id_unsubscribe == form.id_unsubscribe)
            .returning(Unsubscribe))
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_unsubscribe',
             response_model=UnsubscribeDB,
             summary="Delete Unsubscribe",
             description="Delete a unsubscribe from database")
async def delete_unsubscribe(*, request: Request, form: RemoveUnsubscribeDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(Unsubscribe)
        .where(Unsubscribe.id_unsubscribe == form.id_unsubscribe)
    )
    await db.execute(stmt)
