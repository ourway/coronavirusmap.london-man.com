from celery import Celery
from config import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS
from scripts import populate
from core.email import send_simple_message


scheduler = Celery(
    "scheduler",
    broker=f"pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit//",
    result_backend="rpc://",
)


@scheduler.task
def get_postcodes_task():
    return populate.get_postcodes()


@scheduler.task
def emailAgent(email, subject, message):
    send_simple_message(email, subject, message)
