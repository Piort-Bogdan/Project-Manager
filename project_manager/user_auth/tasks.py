import subprocess

from config.celery_app import app
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls remove_expired_tokens_from_db every day at midnight
    sender.add_periodic_task(crontab(minute='0', hour='0'),
                             remove_expired_tokens_from_db.s(),
                             name='remove_expired_tokens_from_db')


@app.task
def remove_expired_tokens_from_db():
    subprocess.run(['python', 'manage.py', 'flushexpiredtokens'])
