from app.utils.db import BaseModel
from peewee import IntegerField, TextField


class Stream(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField(unique=True)
    address = TextField()
    protocol = TextField()
    transport = TextField()

    class Meta:
        table_name = 'streams'
