from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Wrapper
from schemas.wrapper import (AddWrapperDB, DeleteWrapperDB, EditWrapperDB,
                             WrapperDB)

router = APIRouter(prefix='/wrapper')


@router.get('/get_wrappers',
            response_model=list[WrapperDB],
            summary="Get wrapper",
            description="Get wrapper from database")
async def get_wrappers(skip: Annotated[int, Query(description='Pagination skip size', ge=1)] = 0,
                       limit: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
                       db: AsyncSession = Depends(get_db)):
    query = select(Wrapper).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_wrapper', response_model=WrapperDB,
             summary="Add wrapper",
             description="Add wrapper to database")
async def add_wrapper(*, request: Request, form: AddWrapperDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Wrapper).values(*form.dict()).returning(Wrapper)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/update_wrapper', response_model=WrapperDB,
             summary="Update wrapper",
             description="Update wrapper in database")
async def update_wrapper(*, request: Request, form: EditWrapperDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_wrapper']
    stmt = (update(Wrapper)
            .values(*v)
            .where(Wrapper.id_wrapper == form.id_wrapper)
            .returning(Wrapper))
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_wrapper',
             summary="Delete a wrapper",
             description="Delete wrapper from database")
async def delete_wrapper(*, request: Request, form: DeleteWrapperDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(WrapperDB)
        .where(Wrapper.id_wrapper == form.id_wrapper)
    )
    await db.execute(stmt)
