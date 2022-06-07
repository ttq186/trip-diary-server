from celery import Celery

from core.config import settings
import utils

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task
def remind_trip(to_email, start_date, remind_link: str | None = None):
    if remind_link is not None:
        utils.send_remind_trip_email(
            to_email=to_email,
            start_date=start_date,
            remind_link=remind_link,
        )
    else:
        utils.send_remind_trip_email_again(to_email=to_email, start_date=start_date)
