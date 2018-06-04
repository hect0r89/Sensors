from django.contrib import admin

from .models import SensorConfiguration, Sensor

admin.site.register(SensorConfiguration)
admin.site.register(Sensor)
