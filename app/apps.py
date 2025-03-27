# home/apps.py
from django.apps import AppConfig

class HomeConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals