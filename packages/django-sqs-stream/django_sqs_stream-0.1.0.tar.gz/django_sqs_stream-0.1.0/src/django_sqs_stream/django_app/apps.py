from django.apps import AppConfig


class DjangoStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_sqs_stream.django_app"
