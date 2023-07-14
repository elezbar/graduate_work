from abc import ABCMeta, abstractmethod
from sheduler.core.schema import CommentModel, LikesModel, NewsModel
from sheduler.models.models import Notification


class NotificationsABC(metaclass=ABCMeta):

    @abstractmethod
    async def get_notifications_from_db(self, session, event_id: int, event_name: str) -> None:
        """Планово берёт из базы все уведомления, которые необходимо отслеживать."""
        pass
    
    @abstractmethod
    async def iterate_notifications(self, notifications: list) -> None:
        """Перебирает все уведомления, и ставит задачи на проверку."""
        pass
      
    @abstractmethod
    async def check_update_task(self, notification: Notification) -> None:
        """Осуществляет проверку уведомления в таске."""
        pass
    
    @abstractmethod
    async def update_notifications_in_db(self, session, notification: Notification, result: dict) -> None:
        """Обновляет уведомление в БД."""
        pass
    
    @abstractmethod
    async def send_upadte_to_api(self, notification: Notification, data: dict) -> None:
        """Отправляет уведомление в API сервис."""
        pass


class NotificationsParserABC(metaclass=ABCMeta):

    @abstractmethod
    def likses_parser() -> LikesModel | None:
        """Проверяет ответ от UGS сервиса."""
        pass
    
    @abstractmethod
    def comments_parser() -> CommentModel | None:
        """Проверяет ответ от UGS сервиса."""
        pass

    @abstractmethod
    def news_parser() -> NewsModel | None:
        """Проверяет ответ от UGS сервиса."""
        pass
