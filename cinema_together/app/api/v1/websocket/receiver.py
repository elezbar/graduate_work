import json

from core.broadcast import broadcast
from services.utils import check_temp_token, get_cached_message, messages_paginator, set_cached_message
from services.room import get_room_service, async_pg_engine


async def chatroom_ws_receiver(websocket, chatroom):
    async for message in websocket.iter_text():
        received_message = json.loads(message)
        try:
            if received_message['token']:
                db = get_room_service(async_pg_engine)
                new_token = await check_temp_token(received_message, db)
                if new_token:
                    if received_message['type'] == 'slider_info':
                        cached_message = await get_cached_message(chatroom)
                        cached_message['slider'] = received_message['value']
                        await set_cached_message(chatroom, cached_message)
                    else:
                        await broadcast.publish(channel=chatroom, message=message)
                    await websocket.send_text(json.dumps({
                        'type': 'new_token',
                        'username': received_message['username'],
                        'new_token': new_token,
                    }))
        except KeyError:
            continue


async def chatroom_ws_receiver_test(websocket, chatroom):
    async for message in websocket.iter_text():
        received_message = json.loads(message)
        try:
            if received_message['token']:
                # new_token = await check_temp_token(received_message, None)
                new_token = 'qweqweqweqweqweqweqwe123'
                if new_token:
                    if received_message['type'] == 'slider_info':
                        cached_message = await get_cached_message(chatroom)
                        cached_message['slider'] = received_message['value']
                        await set_cached_message(chatroom, cached_message)
                    elif received_message['type'] == 'chat_page':
                        cached_message = await get_cached_message(chatroom)
                        massage = await messages_paginator(chatroom, received_message, cached_message)
                        await websocket.send_text(json.dumps(massage))
                    else:
                        await broadcast.publish(channel=chatroom, message=message)
                    await websocket.send_text(json.dumps({
                        'type': 'new_token',
                        'username': received_message['username'],
                        'new_token': new_token,
                    }))
        except KeyError:
            continue
