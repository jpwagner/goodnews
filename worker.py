### load settings and apps ###
import django               ##
django.setup()              ##
##############################

import os
import redis
from rq import Worker, Queue, Connection

conn = redis.from_url(os.getenv('BROKER_URL'))

listen = ['default']

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()