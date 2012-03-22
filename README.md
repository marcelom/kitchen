# Kitchen

Kitchen is a Dashboard where you can visualize and browse your servers.
It never has been so easy to find and orginize all your nodes!

## How it works

Data is taken from a Chef repository's node data bag

## Installation

We will need:

* sqlite (or another celery broker)
* python 2.6+
* Django 1.3+
* django-celery and django-kombu
* Littlechef

`apt-get install sqlite3`

`pip install django django-celery django-kombu`

`pip install littlechef`

Then create the necessary celery tables

`python manage.py syncdb`

## Running the development server and job queue

To see the web interface on localhost:8000:

`python manager.py runserver`

To start the celerybeat job scheduler

`python manage.py celeryd -B -l info`
