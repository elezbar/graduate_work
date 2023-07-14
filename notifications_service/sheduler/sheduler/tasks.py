import asyncio

from sheduler.celery import app
from celery.utils.log import get_task_logger

from sheduler.core.config import config
from sheduler.schedule import Notifications

logger = get_task_logger(__name__)


@app.task
def check_likes():
    try:
        likes = Notifications(config.constants.likes_event_id, 'likes')
        asyncio.run(likes.get_notifications_from_db())
    except Exception as e:
        logger.error(e)

@app.task
def check_comments():
    try:
        likes = Notifications(config.constants.comments_event_id, 'comments')
        asyncio.run(likes.get_notifications_from_db())
    except Exception as e:
        logger.error(e)


@app.task
def check_news():
    try:
        likes = Notifications(config.constants.news_event_id, 'news')
        asyncio.run(likes.get_notifications_from_db())
    except Exception as e:
        logger.error(e)
