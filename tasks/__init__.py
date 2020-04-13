from celery import Celery
from config import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS
from scripts import populate


scheduler = Celery(
    "scheduler",
    broker=f"pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit//",
    result_backend="rpc://",
)


@scheduler.task
def get_postcodes_task():
    return populate.get_postcodes()
