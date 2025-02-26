from cache_register import register

from django_sqs_stream.django_app.base import handler, serializer

serializers = register.Register[serializer.EventSerializer]("serializers")
handlers = register.Register[handler.Handler]("handlers")
