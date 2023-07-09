import json

from core.broadcast import broadcast
from services.utils import decode_token, get_cached_message, set_cached_message


async def chatroom_ws_receiver(websocket, chatroom):
    async for message in websocket.iter_text():
        received_message = json.loads(message)
        try:
            if received_message['token']:
                decoded_token = decode_token(received_message['token'])
                if decoded_token:
                    if received_message['type'] == 'slider_info':
                        cached_message = await get_cached_message(chatroom)
                        cached_message['slider'] = received_message['value']
                        await set_cached_message(chatroom, cached_message)
                    else:
                        await broadcast.publish(channel=chatroom, message=message)
        except KeyError:
            continue


async def chatroom_ws_receiver_test(websocket, chatroom):
    async for message in websocket.iter_text():
        received_message = json.loads(message)
        try:
            if received_message['token']:
                if received_message['type'] == 'slider_info':
                    cached_message = await get_cached_message(chatroom)
                    cached_message['slider'] = received_message['value']
                    await set_cached_message(chatroom, cached_message)
                else:
                    await broadcast.publish(channel=chatroom, message=message)
        except KeyError as e:
            continue
