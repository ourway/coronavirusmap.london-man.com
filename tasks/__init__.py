from celery import Celery


scheduler = Celery(
    "scheduler", broker="pyamqp://admin:u2KzPCReW2B@rabbit//", result_backend="rpc://"
)


@scheduler.task
def add(x, y):
    return x + y
