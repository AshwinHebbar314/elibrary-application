from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_cors import CORS

from appln.initialize import celery_init_app
from appln.worker import daily_reminder_email, user_monthly_report, auto_return_books
from celery.schedules import crontab

app = Flask(__name__)


def create_app():

    from appln.views import view
    from appln.models import User, Role, UserRoles, db
    from werkzeug.security import generate_password_hash # for password hashing
    from appln import initialize

    # caching imports
    from appln.cache import cache

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite3'
    # set secret key
    app.config['SECRET_KEY'] = 'super-secret'
    # is this really reqd?
    app.config['WTF_CSRF_ENABLED'] = False
    # set up celery
    app.config['CELERY'] = {
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
        'enable_utc': True,
        'timezone': 'UTC',
    }

    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)


    app.register_blueprint(view)
    
    CORS(app)
    cache.init_app(app, {   
                            "CACHE_TYPE": "RedisCache",
                            "CACHE_DEFAULT_TIMEOUT": 10,
                            "CACHE_REDIS_URL": "redis://localhost:6379"
                        }
                )

    with app.app_context():
        db.create_all()

        initialize.main()
    
    return app


app = create_app()

celery = celery_init_app(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, daily_reminder_email.s(), name='Email to send daily reminders')
    sender.add_periodic_task(10, user_monthly_report.s(), name='Monthly user report')
    # sender.add_periodic_task(10, user_monthly_report.s(), name='Monthly user report')
    sender.add_periodic_task(crontab(minute="*"), auto_return_books.s(), name='Auto return books')