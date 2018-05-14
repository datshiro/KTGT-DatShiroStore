from django.apps import AppConfig


class DatshiroshopConfig(AppConfig):
    name = 'DatShiroShop'

    def ready(self):
        import DatShiroShop.signals