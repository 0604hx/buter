from flask import Flask, config
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'buter.schedule.jobs:interval',
            'args': (),
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    config.Config

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()