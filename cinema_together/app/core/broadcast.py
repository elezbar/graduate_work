from broadcaster import Broadcast

from core.config import settings


broadcast = Broadcast(f'redis://{settings.redis_host}:{settings.redis_port}')
