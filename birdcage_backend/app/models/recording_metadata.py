from app.utils.db import BaseModel
from peewee import IntegerField, TextField, DateTimeField
import datetime

class RecordingMetadata(BaseModel):
    id = IntegerField(primary_key=True)
    filename = TextField(unique=True)
    stream_id = IntegerField()
    streamname = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)