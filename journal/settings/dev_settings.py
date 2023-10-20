from .base_settings import *


SECRET_KEY = 'lksdjcoiwhviuhvv943g94hf04v9hf09vf'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
