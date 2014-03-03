from django.contrib import admin
from plants.models import Arugula

class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'initial_date', 'temperature', 'light_intensity', 'nutrient_density']
    fields       = ['initial_date', 'temperature', 'light_intensity', 'nutrient_density']

admin.site.register(Arugula, PlantAdmin)