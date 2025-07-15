web: german_app.wsgi:application --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn test_project.wsgi
