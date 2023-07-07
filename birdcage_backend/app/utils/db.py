from peewee import SqliteDatabase, Model
from config import DATABASE_FILE

db = SqliteDatabase(DATABASE_FILE)


class BaseModel(Model):
    class Meta:
        database = db
