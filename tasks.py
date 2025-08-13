from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def superuser(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp transactions")


@task
def celery(c):
    c.run("celery -A root worker --loglevel=info --pool=solo")
