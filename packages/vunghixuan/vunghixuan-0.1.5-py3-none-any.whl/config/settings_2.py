# config/settings.py

DATABASE_CONFIG = {
    'HOST': 'localhost',
    'PORT': 5432,
    'USER': 'your_username',
    'PASSWORD': 'your_password',
    'DB_NAME': 'your_database'
}

APPS = [
    'apps.app_mainGui'
    # 'apps.users',
    # 'apps.products',
    # 'apps.orders'
]

def register_apps():
    for app in APPS:
        __import__(app)

def get_model(app_name, model_name):
    app = __import__(app_name)
    return getattr(app.models, model_name)
