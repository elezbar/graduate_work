import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import Request

from core.decorators import login_required
from services.room import RoomService, get_room_service
from services.utils import create_room_link

router = APIRouter()
bearer_token = HTTPBearer()


@router.post('/')
@login_required()
async def create_room(
        request: Request,
        service: RoomService = Depends(get_room_service),
):
    room_id = uuid.uuid4()
    film_id = uuid.uuid4()
    link = create_room_link(room_id)
    error = await service.create_room(
        room_id=room_id,
        user_id=request.user.pk,
        link=link,
        film_id=film_id
    )
    if error:
        return {'success': False, 'errors': list(error)}
    return {'success': True, 'link': link}


@router.get('/{room_id}/connect')
@login_required()
async def join_user(
        request: Request,
        room_id: str,
        service: RoomService = Depends(get_room_service)
):
    error = await service.connect(user=request.user, room_id=room_id)
    if error:
        return {'connection': False, 'errors': list(error)}

    return {'connection': 'success'}


@router.post('/{room_id}/disconnect')
@login_required()
async def disconnect_user(
        request: Request,
        room_id: str,
        service: RoomService = Depends(get_room_service)
):

    result = await service.disconnect_user(user=request.user, room_id=room_id)

    if not result:
        return {'disconnect user': False}

    return {'disconnect user': True}
