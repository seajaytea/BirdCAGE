from app.utils.db import BaseModel
from peewee import IntegerField, FloatField, TextField, ForeignKeyField

class FilterThresholds(BaseModel):
    user_id = IntegerField(primary_key=True)
    ignore_threshold = FloatField()
    log_threshold = FloatField()
    recordalert_threshold = FloatField()

    class Meta:
        table_name = 'filter_thresholds'

    @classmethod
    def create_table(cls, safe=True):
        super().create_table(cls)

        init = cls.select().where(cls.user_id == 0).first()
        if init:
            return
        cls.create(user_id=0, ignore_threshold=1, log_threshold=1, recordalert_threshold=0).save()

class SpeciessOverides(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(FilterThresholds, backref='species_overrides')
    species_name = TextField()
    override_type = TextField()

    class Meta:
        table_name = 'species_overrides'

        indexs = (
            (('user_id', 'species_name'), True),
        )