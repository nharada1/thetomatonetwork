from django.contrib import admin
from plants.models import English_Ivy
from plants.models import Plant_State

class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'initial_date', 'user_name', 'plant_name']
    fields       = ['initial_date', 'user_name', 'plant_name']

class PlantStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestep', 'date', 'nutrient_value', 'light_value', 'health_rating', 'plant']
    fields       = ['timestep', 'date', 'nutrient_value', 'light_value', 'health_rating', 'plant']

admin.site.register(English_Ivy, PlantAdmin)
admin.site.register(Plant_State, PlantStateAdmin)