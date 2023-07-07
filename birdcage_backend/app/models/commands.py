from app.utils.db import BaseModel
from app.models.preferences import UserPreferences
from peewee import IntegerField, TextField, BooleanField


class Command(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField(unique=True)
    value = BooleanField()

    class Meta:
        table_name = 'commands'
    
    @classmethod
    def create_table(cls, safe=True):
        super().create_table(cls)

        init = cls.get_or_none(cls.name == 'restart')
        if init:
            return
        cls.create(name='restart', value=False).save()