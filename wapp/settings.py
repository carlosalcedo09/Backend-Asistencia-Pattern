
from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from import_export.formats.base_formats import XLSX, CSV, HTML
from django.templatetags.static import static
from django.urls import reverse_lazy
import dj_database_url
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG')))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# Application definition

BASE_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.forms",
    #'multi_captcha_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_better_admin_arrayfield',
    
]


LOCAL_APPS = [
    'apps.subadmin',
    'apps.users.apps.UsersConfig',
    'apps.base.apps.BaseConfig',
    'apps.maintenance',
    'apps.payroll',
    'apps.employees',
    'apps.schedule',
    'apps.attendance'
]

THIRD_APPS = [
    'nested_admin',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'import_export',
    'django_select2',
    'rangefilter',
    'admin_auto_filters',
    'ckeditor',
    #'simple_history',
    #'debug_toolbar',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS 

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'wapp.middleware.CustomPermissionMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'apps.base.middleware.CurrentEmployeeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000","http://localhost:5173",
]

ROOT_URLCONF = 'wapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wapp.wsgi.application'



#DATABASES = {
#    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
#}

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': int(os.getenv('DATABASE_PORT')),
        'CONN_MAX_AGE': 300
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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



AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

#USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_X_FORWARDED_FOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"

# Donde Django colocará los archivos estáticos AL HACER collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Carpeta de tus archivos estáticos locales (CSS, JS, imágenes)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EXPORT_FORMATS = [XLSX, CSV, HTML]

SITE_ID = 1

RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

MULTI_CAPTCHA_ADMIN = {
    'engine': 'recaptcha2',
}

ICON_EDIT_URL = '/static/admin/img/visible.png'


LOGO_URL = 'file:///' + os.path.join(BASE_DIR, 'static', 'admin', 'img', 'logo-pattern.jpeg').replace('\\', '/')


LOGIN_URL = '/admin/login/'

INTERNAL_IPS = [
    '127.0.0.1',
]


UNFOLD = {
    "SITE_TITLE": 'Sistema de asistencia',
    "SITE_HEADER": " ",
    "SITE_URL": "https://pattern.pe/",
    "THEME": "light",
    "SITE_ICON": "/static/admin/img/logo-pattern.png",
    "STYLES": [
        lambda request: static("admin/css/admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("admin/js/jquery-3.6.0.min.js"),
    ],
    "LOGIN": {
         "image": "https://centenariooficinas.pe/wp-content/uploads/2023/11/real-1-1.jpg",
         #"redirect_after": lambda r: reverse_lazy("admin:project_project_changelist"),
    },
    "COLORS": {
        "primary": {
        "50": "100 100 100",
        "100": "100 100 100",
        "200": "100 100 100",
        "300": "100 100 100",
        "400": "100 100 100",
        "500": "100 100 100",
        "600": "100 100 100",
        "700": "100 100 100",
        "800": "100 100 100",
        "900": "100 100 100",
        "950": "100 100 100"
    }
    }, 
    #"SITE_ICON": "https://seguridad.apps-andina.com/img/logo-confipetrol-dark.7e355b3b.jpg",
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Seguridad",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": "Permisos",
                        "icon": "lock",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    }
                    
                ],
            },
            {
                "title": "Empleados",
                "separator": True,
                "items": [
                    {
                        "title": "Colaboradores",
                        "icon": "person",
                        "link": reverse_lazy("admin:employees_employee_changelist"),
                    },
                ],
            },
            {
                "title": "Gestión de horarios",
                "separator": True,
                "items": [
                    {
                        "title": "Asignación de Horarios",
                        "icon": "schedule",
                        "link": reverse_lazy("admin:schedule_schedule_detail_changelist"),
                    },
                    {
                        "title": "Horarios laborales",
                        "icon": "schedule",
                        "link": reverse_lazy("admin:schedule_schedule_changelist"),
                    },
                ],
            },
            {
                "title": "Gestión de asistencia",
                "separator": True,
                "items": [
                    {
                        "title": "Asistencias",
                        "icon": "business_center",
                        "link": reverse_lazy("admin:attendance_attendance_changelist"),
                    },
                    {
                        "title": "Resumen de marcaciones",
                        "icon": "business_center",
                        "link": reverse_lazy("admin:attendance_attendancemarking_changelist"),
                    }
                ],
            },
            {
                "title": "Gestión de nómina",
                "separator": True,
                "items": [
                    {
                        "title": "Nóminas",
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:payroll_payroll_changelist"),
                    },
                ],
            },
            {
                "title": "Maestros",
                "separator": True,
                "items": [
                    
                    {
                        "title": "Áreas",
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:maintenance_area_changelist"),
                    },
                    {
                        "title": "Cargos",
                        "icon": "business_center",
                        "link": reverse_lazy("admin:maintenance_position_changelist"),
                    },
                    {
                        "title": "Conceptos",
                        "icon": "view_list",
                        "link": reverse_lazy("admin:maintenance_concept_changelist"),
                    },
                    {
                        "title": "Parámetros",
                        "icon": "tune",
                        "link": reverse_lazy("admin:maintenance_parameter_changelist"),
                    },
                    {
                        "title": "Tipo de marcación",
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:maintenance_type_marking_changelist"),
                    },
                    {
                        "title": "Tipo de Justificaión",
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:maintenance_type_justification_changelist"),
                    },
                ],
            },
        ],
    },
}



CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            ['bold', 'italic', 'underline'],
            ['link', 'image'],
            ['undo', 'redo'],
        ],
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', 
    ),
}

SIMPLE_JWT = {
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}