from celery import Celery

DB_NAME = "CeleryTask"
MONGODB_URL = "mongodb://localhost:27017/"

# mongodb connection string
MONGODB_CON_STR = "{}{}".format(MONGODB_URL, DB_NAME)
app = Celery('celery_task_monitor',
             broker=MONGODB_CON_STR,
             backend=MONGODB_CON_STR,
             include=['celery_task_monitor.tasks'])

if __name__ == '__main__':
    app.start()