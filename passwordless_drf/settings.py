
import os
from decouple import config



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['passwordlessdrf.pythonanywhere.com']


AUTH_USER_MODEL = 'accounts.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    #internal apps
    'accounts',
    'certify',




    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'passwordless_drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'passwordless_drf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR,'mediafiles')
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)



PASSWORDLESS_AFRICAS_TALKING_USERNAME =config('PASSWORDLESS_AFRICAS_TALKING_USERNAME')

PASSWORDLESS_AFRICAS_TALKING_API_KEY=config('PASSWORDLESS_AFRICAS_TALKING_API_KEY')

PASSWORDLESS_AFRICAS_TALKING_SENDER_ID = config('PASSWORDLESS_AFRICAS_TALKING_SENDER_ID')


PASSWORDLESS_TOKEN_EXPIRE_TIME=  1 * 60

DEFAULTS = {

    # Allowed auth types, can be EMAIL, MOBILE, or both.
    'PASSWORDLESS_AUTH_TYPES': ['EMAIL'],

    # Amount of time that tokens last, in seconds
    'PASSWORDLESS_TOKEN_EXPIRE_TIME': 15 * 60,


    



    # The email the callback token is sent from
    'PASSWORDLESS_EMAIL_NOREPLY_ADDRESS': None,

    # The email subject
    'PASSWORDLESS_EMAIL_SUBJECT': "Your Login Token",

    # A plaintext email message overridden by the html message. Takes one string.
    'PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE': "Enter this token to sign in: %s",

    # The email template name.
    'PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME': "passwordless_default_token_email.html",

    # Your twilio number that sends the callback tokens.
    'PASSWORDLESS_MOBILE_NOREPLY_NUMBER': None,

    # The message sent to mobile users logging in. Takes one string.
    'PASSWORDLESS_MOBILE_MESSAGE': "Use this code to log in: %s",

    # Registers previously unseen aliases as new users.
    'PASSWORDLESS_REGISTER_NEW_USERS': True,



    

    # The verification email subject
    'PASSWORDLESS_EMAIL_VERIFICATION_SUBJECT': "Your Verification Token",

    # A plaintext verification email message overridden by the html message. Takes one string.
    'PASSWORDLESS_EMAIL_VERIFICATION_PLAINTEXT_MESSAGE': "Enter this verification code: %s",

    # The verification email template name.
    'PASSWORDLESS_EMAIL_VERIFICATION_TOKEN_HTML_TEMPLATE_NAME': "passwordless_default_verification_token_email.html",

    # The message sent to mobile users logging in. Takes one string.
    'PASSWORDLESS_MOBILE_VERIFICATION_MESSAGE': "Enter this verification code: %s",


}





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/out.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/main_debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'null': {
            "class": 'logging.NullHandler', #'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}

