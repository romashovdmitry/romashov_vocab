''' File for Heroku: to set webhook on schedule '''
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=10)
def timed_job():
    requests.post('https://api.telegram.org/bot<token>/deleteWebhook')
    requests.post('https://api.telegram.org/bot<token>/setWebhook?url=<URL that get \
                requests from Telegram server>')

sched.start()