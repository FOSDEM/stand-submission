from datetime import datetime
from pytz import timezone

SECRET_KEY = ''

##
# Edition
##
EDITION = '2023'
DIGITAL_EDITION = False

##
# Deadlines
##
SUBMISSION_DEADLINE = datetime(
    2020,
    11,
    15,
    tzinfo=timezone('Europe/Brussels')
)
ANNOUNCEMENT_DATE = datetime(
    2020,
    12,
    1,
    tzinfo=timezone('Europe/Brussels')
)

##
# Database stuff
##
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stands',
        'USER': 'stands',
        'PASSWORD': 'stands',
        'HOST': 'db',
        'PORT': '5432'
    }
}

##
# Mailing
##
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
