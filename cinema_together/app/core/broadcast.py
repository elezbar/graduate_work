from broadcaster import Broadcast

from core.config import settings


broadcast = Broadcast(f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')
