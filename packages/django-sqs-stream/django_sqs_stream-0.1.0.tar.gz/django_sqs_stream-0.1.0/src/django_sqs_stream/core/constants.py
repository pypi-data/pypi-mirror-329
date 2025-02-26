import enum


class EventType(enum.StrEnum):
    TEST_EVENT = "TEST.EVENT"


class AWSClient(enum.StrEnum):
    SQS = "sqs"


class InboundEventStatus(enum.StrEnum):
    PENDING = "PENDING"
    HANDLED = "HANDLED"
    FAILED = "FAILED"


class OutboundEventStatus(enum.StrEnum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
