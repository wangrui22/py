import time
from celery import Celery
import celery_config

app = Celery('tasks', backend="amqp", broker="amqp://")

@app.task
def add(x,y):
    time.sleep(5)
    return x + y