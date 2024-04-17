from flask import Flask, current_app as app
from werkzeug.security import generate_password_hash
from appln.models import db
from celery import Celery, Task

def main():
    if not app.security.datastore.find_role("admin"):

    # Define Roles here, associated function: find_role, create_user, add_role_to_user
        admin = app.security.datastore.create_role(name='admin', description='Administrator Account')
        app.security.datastore.create_role(name='user', description='User Account')


        db.session.flush()

        user = app.security.datastore.create_user(fname = "John",
                                        lname = "Doe",
                                        uname = "admin",
                                        email = "admin@elib.com",
                                        password = generate_password_hash("admin"),
        )

        app.security.datastore.add_role_to_user(user, admin)
        db.session.commit()

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app