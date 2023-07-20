import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import Header, Request

from core.decorators import login_required
from models.scheme import RoomModel
from services.room import RoomService, get_room_service
from services.utils import create_room_link, send_invitation

router = APIRouter()
bearer_token = HTTPBearer()


@router.post('/')
@login_required()
async def create_room(
        room: RoomModel,
        authorizations: str | None = Header(default=None, convert_underscores=False),
        service: RoomService = Depends(get_room_service),
):
    room_id = uuid.uuid4()
    link = create_room_link(room_id)
    error = await service.create_room(
        room_id=room_id,
        user_id=room.creator_id,
        link=link,
        film_id=room.film_id,
        members=room.members
    )
    if error:
        return {'success': False, 'errors': [error]}
    if room.members:
        await send_invitation(link, room.members, authorizations)
    return {'success': True, 'link': link}


@router.get('/{room_id}/join')
@login_required()
async def join_user(
        request: Request,
        room_id: str,
        authorizations: str | None = Header(default=None, convert_underscores=False),
        service: RoomService = Depends(get_room_service)
):
    error = await service.connect(user=request.user, room_id=room_id)
    if error:
        return {'connection': False, 'errors': [error]}
    return {'connection': 'success'}


@router.post('/{room_id}/disconnect')
@login_required()
async def disconnect_user(
        request: Request,
        room_id: str,
        authorizations: str | None = Header(default=None, convert_underscores=False),
        service: RoomService = Depends(get_room_service)
):

    result = await service.disconnect_user(user=request.user, room_id=room_id)

    if not result:
        return {'disconnect user': False}

    return {'disconnect user': True}
