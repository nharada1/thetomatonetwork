from django.contrib import admin
from plants.models import EnglishIvy
from plants.models import PlantState
from plants.models import AlgoMetadata


class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'initial_date', 'user_name', 'plant_name']
    fields       = ['initial_date', 'user_name', 'plant_name']


class PlantStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestep', 'date', 'nutrient_value', 'light_value', 'performance_value', 'plant']
    fields       = ['timestep', 'date', 'nutrient_value', 'light_value', 'performance_value', 'plant']


class AlgoMetaDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'L', 'T', 'tau']
    fields       = ['date', 'L', 'T', 'tau']

admin.site.register(EnglishIvy, PlantAdmin)
admin.site.register(PlantState, PlantStateAdmin)
admin.site.register(AlgoMetadata, AlgoMetaDataAdmin)
