from app.utils.db import BaseModel
from peewee import IntegerField, TextField, DateTimeField
import datetime

import sqlite3
import bcrypt
from config import DATABASE_FILE


class UserPreferences(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    preference_key = TextField()
    preference_value = TextField()
    last_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexs = (
            (('user_id', 'preference_key'), True),
        )
        table_name = 'user_preferences'

    @classmethod
    def get_all_user_preferences(cls, user_id):
        rtn = {}
        preferences = cls.select().where(cls.user_id == user_id)
        
        for preference in preferences:
            rtn[preference.preference_key] = preference.preference_value
        return rtn

    
    #method to populate initial data
    @classmethod
    def create_table(cls, safe=True):
        super().create_table(cls)
        #check if already init
        init = cls.get_or_none(cls.preference_key == 'init')
        if init:
            return
        #create default preferences
        password = 'birdcage'
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        #create default preferences
        default_preferences = [
            ('init', 'true'),
            ('recordinglength', '15'),
            ('confidence', '0.7'),
            ('extractionlength', '6'),
            ('latitude', '39.0473'),
            ('longitude', '-95.6752'),
            ('overlap', '0'),
            ('sensitivity', '1'),
            ('sf_thresh', '0.03'),
            ('password', hashed_password),
            ('locale', 'en'),
            ('recordingretention', '0'),
            ('mqttbroker', ''),
            ('mqttport', '1883'),
            ('mqttuser', ''),
            ('mqttpassword', ''),
            ('mqttrecordings', 'false')
        ]


        for key, value in default_preferences:
            cls.create(user_id=0, preference_key=key, preference_value=value, last_updated=datetime.datetime.now()).save()


def check_password(password_input):
    # Retrieve the hashed password from the database
    hashed_password = UserPreferences.get(UserPreferences.preference_key == 'password').preference_value

    # Verify the input password against the stored hashed password
    return bcrypt.checkpw(password_input.encode(), hashed_password.encode())