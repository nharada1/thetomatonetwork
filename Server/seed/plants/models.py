from django.db import models

class Plant(models.Model):
    initial_date     = models.DateTimeField('Age')
    temperature      = models.FloatField('Temperature')
    nutrient_density = models.FloatField('Nutrient Density')
    light_intensity  = models.FloatField('Light Intensity')

    class Meta:
        abstract = True

class Arugula(Plant):
    pass