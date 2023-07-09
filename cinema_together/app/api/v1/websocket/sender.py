import json

from core.broadcast import broadcast
from services.utils import get_cached_message, modify_cached_message, set_cached_message


async def chatroom_ws_sender(websocket, chatroom):
    async with broadcast.subscribe(channel=chatroom) as subscriber:
        async for event in subscriber:
            event_message = json.loads(event.message)
            cached_message = await get_cached_message(chatroom)
            modified_cached_message = await modify_cached_message(event_message, cached_message)
            if event_message['type'] not in ['initial_request', 'initial_response']:
                await websocket.send_text(json.dumps(event_message))
                await set_cached_message(chatroom, modified_cached_message)
            elif event_message['type'] == 'initial_request':
                await chatroom_send_initial(modified_cached_message, websocket)


async def chatroom_send_initial(modified_cached_message, websocket):
    await websocket.send_text(json.dumps(modified_cached_message))
