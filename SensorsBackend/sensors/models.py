from django.db import models


class Sensor(models.Model):

    id_sensor = models.CharField(max_length=150)
    acquisition_date = models.DateField('acquisition date')
    signal_type = models.CharField(max_length=150)
    reading_value = models.FloatField(default=0.0)
    reading_date = models.DateField('reading date')
    __previous_acquisition_date = None

    class Meta:
        unique_together = ('id_sensor', 'reading_date', 'signal_type')

    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)
        self.__previous_acquisition_date = self.acquisition_date

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            if self.__previous_acquisition_date < self.acquisition_date:
                super().save(force_insert, force_update, using, update_fields)
                self.__previous_acquisition_date = self.acquisition_date
        else:
            super().save(force_insert, force_update, using, update_fields)
            self.__previous_acquisition_date = self.acquisition_date


class SensorConfiguration(models.Model):
    COUNT = 'count'
    MEAN = 'mean'
    MEDIAN = 'median'
    MIN = 'min'
    MAX = 'max'
    STD = 'std'
    VAR = 'var'
    MAD = 'mad'
    PROD = 'prod'
    SUM = 'sum'
    CALC_TYPES_CHOICES = (
        (COUNT, 'count'),
        (MEAN, 'mean'),
        (MEDIAN, 'median'),
        (MIN, 'min'),
        (MAX, 'max'),
        (STD, 'std'),
        (VAR, 'var'),
        (MAD, 'mad'),
        (PROD, 'prod'),
        (SUM, 'sum')
    )
    id_signal = models.CharField(max_length=150, primary_key=True, unique=True)
    signal_type = models.CharField(max_length=5, choices=CALC_TYPES_CHOICES, default=MEAN)
