import json

from core.broadcast import broadcast
from services.utils import get_cached_message, set_cached_message


async def chatroom_ws_receiver(websocket, chatroom):
    async for message in websocket.iter_text():
        received_message = json.loads(message)
        if received_message['type'] == 'slider_info':
            cached_message = await get_cached_message(chatroom)
            cached_message['slider'] = received_message['value']
            await set_cached_message(chatroom, cached_message)
        else:
            await broadcast.publish(channel=chatroom, message=message)
