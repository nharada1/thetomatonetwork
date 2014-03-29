from django.contrib import admin
from plants.models import EnglishIvy
from plants.models import PlantState
from plants.models import ControlPlantState
from plants.models import AlgoMetadata
from plants.models import CareConstants


class PlantAdmin(admin.ModelAdmin):
   list_display = ['id', 'initial_date', 'is_control', 'user_name', 'plant_name']
   fields       = ['initial_date', 'is_control', 'user_name', 'plant_name']

class PlantStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestep', 'date', 'nutrient_value', 'light_value', 'performance_value', 'plant']
    fields       = ['timestep', 'date', 'nutrient_value', 'light_value', 'performance_value', 'plant']

class ControlPlantStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestep', 'date', 'performance_value', 'plant']
    fields       = ['timestep', 'date', 'performance_value', 'plant']


class AlgoMetaDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'L', 'T', 'tau']
    fields       = ['date', 'L', 'T', 'tau']

class CareConstantsAdmin(admin.ModelAdmin):
    list_display = ['id','water_cycle_period','light_start_hour','light_end_hour']
    fields = ['water_cycle_period','light_start_hour','light_end_hour']

admin.site.register(EnglishIvy, PlantAdmin)
admin.site.register(PlantState, PlantStateAdmin)
admin.site.register(ControlPlantState, ControlPlantStateAdmin)
admin.site.register(AlgoMetadata, AlgoMetaDataAdmin)
admin.site.register(CareConstants, CareConstantsAdmin)
