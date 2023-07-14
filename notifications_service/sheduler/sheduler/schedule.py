
import asyncio
import orjson

from collections.abc import Sequence as Sq
from datetime import datetime, timedelta
from sqlalchemy import select

from sheduler.core import utils
from sheduler.core.config import config
from sheduler.core.logger import get_logger
from sheduler.models.models import Notification
from sheduler.postgres.db import session
from sheduler.core.schema import CommentModel, ConfigMixin, LikesModel, NewsModel
from sheduler.schedule_abstract import NotificationsABC, NotificationsParserABC

logger = get_logger(__name__)


class Notifications(NotificationsABC):

    @session
    def __init__(self, event_id: int, event_name: str, session):
        self.session = session
        self.event_id = event_id
        self.event_name = event_name

    async def get_notifications_from_db(self) -> None:
        toDate = datetime.now() - timedelta(days=14)
        stmt = (
            select(Notification)
            .where(Notification.id_event == self.event_id)
            .where(Notification.last_update > toDate)
            .where(Notification.last_update > Notification.last_notification_send).limit(50)
        )
        asyncio.run(self.iterate_notifications(self.session.scalars(stmt)))
    
    async def iterate_notifications(self, notifications: Notification) -> None:
        """Перебирает все уведомления, и ставит задачи на проверку."""
        async for notification in notifications:
            asyncio.run(self.check_update_task(notification))

    async def check_update_task(self, notification: Notification) -> None:
        """Осуществляет проверку уведомления в таске."""
        parsed_result = False
        url = (
            f'{config.constants.ugs_url}{self.event_name}/'
            f'?id_content={str(notification.id_content)}'
            f'&last-update={str(notification.last_update)}'
        )
        result = asyncio.run(utils.request_get(url))
        if self.id_event == config.constants.likes_event_id:
            parser = NotificationsParser(LikesModel, result)
            parsed_result = parser.likses_parser()
        elif self.id_event == config.constants.comments_event_id:
            parser = NotificationsParser(CommentModel, result)
            parsed_result = parser.comments_parser()
        elif self.id_event == config.constants.news_event_id:
            parser = NotificationsParser(NewsModel, result)
            parsed_result = parser.news_parser()
        if parsed_result:
            await self.send_upadte_to_api(notification, parsed_result)
        
    async def update_notifications_in_db(self, session, notification: Notification, result: dict) -> None:
        """Обновляет уведомление в БД."""
        notification.last_notification_send = datetime.now()
        session.commit()
    
    async def send_upadte_to_api(self, notification: Notification, data: dict) -> None:
        """Отправляет уведомление в API сервис."""
        url = config.constants.notifications_url
        if self.id_event == config.constants.news_event_id:
            url = config.constants.news_url
        result = asyncio.run(utils.request_post(url, data))
        if result:
            if result['result'] == 'ok':
                await self.update_notifications_in_db(notification, result)


class NotificationsParser(NotificationsParserABC):

    def __init__(self, model: ConfigMixin, data: dict):
        self.model = model
        self.data = data

    def likses_parser(self):
        try:
            return self.model.parse_obj(self.data)
        except Exception as e:
            logger.error(f'Error while parsing Likes object: {e}')
            return None

    def comments_parser(self):
        try:
            objs = self.data.comments
            if isinstance(self.data, Sq):
                return [self.model.parse_obj(obj) for obj in objs]
            return None
        except Exception as e:
            logger.error(f'Error while parsing Comments objects: {e}')
            return None
    
    def news_parser(self):
        try:
            objs = self.data.news
            if isinstance(self.data, Sq):
                return [self.model.parse_obj(obj) for obj in objs]
            return None
        except Exception as e:
            logger.error(f'Error while parsing News objects: {e}')
            return None
