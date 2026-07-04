from django.apps import AppConfig


class EbdConfig(AppConfig):
    name = "ebd"

    def ready(self):
        import ebd.signals  # noqa
