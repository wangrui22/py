import time
from celery import Celery

app = Celery('tasks', backend="amqp", broker="amqp://")

@app.task
def evaluate(data_url):
    time.sleep(5)
    # do evaluation
    print('evaluate %s done.' % data_url)
    # save to db