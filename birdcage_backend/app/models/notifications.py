from app.utils.db import BaseModel
from peewee import ForeignKeyField, TextField

class NotificationService(BaseModel):
    service_name = TextField(unique=True)
    service_url = TextField()

    class Meta:
        table_name = 'notification_services'

    @classmethod
    def create_table(cls, safe=True):
        super().create_table(cls)

        init = cls.get_or_none(cls.service_name == 'Service 1')
        if init:
            return
        cls.create(service_name='Service 1', service_url='').save()
        cls.create(service_name='Service 2', service_url='').save()
        cls.create(service_name='Service 3', service_url='').save()

class NotificationAssignment(BaseModel):
    detectionaction = TextField()
    notification_service = ForeignKeyField(NotificationService, backref='notification_assignments')

    class Meta:
        table_name = 'notification_assignments'