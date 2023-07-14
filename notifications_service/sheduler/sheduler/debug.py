from datetime import datetime, timedelta
from random import randint

from models import models
from postgres.base_model import meta
from postgres.db import engine, session
from schedule import Notifications


@session
def create_db_initial_data(session):
    events = [
        models.Event(id_event=1, name="likes", interval=30),
        models.Event(id_event=2, name="comments", interval=30)
    ]

    toDate = datetime.now() - timedelta(days=1)
    notifications = []
    for num in range(200):
        notifications.append(
            models.Notification(id_notification=num,
                                id_content=randint(1, 4),
                                id_event=randint(1, 2),
                                id_user=randint(10, 100),
                                last_update=datetime.now(),
                                last_notification_send=toDate)
        )
    session.bulk_save_objects(events)
    session.commit()
    session.bulk_save_objects(notifications)
    session.commit()


if __name__ == '__main__':
    meta.create_all(bind=engine)
    create_db_initial_data()

    # likes = Notifications()
    # events = likes.get_all_events_from_db()
    # print(type(events))
    # for event in likes.get_all_events_from_db():
    #     print(event)
