from django.db import models

class Plant(models.Model):
    ''' Plant is a superclass for all different types of plants we end up using
        currently we have boilerplate for:
            - Arugula
            - English Ivy
    '''
    # Plant Metadata
    initial_date     = models.DateTimeField('Birthday')

    # User data
    user_name        = models.CharField("User's Name", max_length=20)
    plant_name       = models.CharField("Plant's Name", max_length=20)

    def __unicode__(self):
        return u"%s's plant %s" % (self.user_name, self.plant_name)


class PlantState(models.Model):
    ''' Plant states represent the different parameters we are keeping track of
        Currently we control nutrient flow, and measure ambient light
    '''
    timestep        = models.IntegerField('Timestep')
    date            = models.DateTimeField('Date-Time')
    nutrient_value  = models.FloatField('Nutrient Value')
    light_value     = models.FloatField('Light Value')
    health_rating   = models.FloatField('Health Rating')
    plant           = models.ForeignKey(Plant)

    def __unicode__(self):
        return u"%s's plant %s's state at time step %d" % (self.plant.user_name, self.plant.plant_name, self.timestep)

class AlgoMetadata(models.Model):
    ''' Metadata for current state/iteration of algorithm. Contains two variables:
        - Lipschitz constant of performance function
        - Expected time of convergence
    '''

    L = models.FloatField('Lipschitz Constant')
    T = models.IntegerField('Time of Convergence')

    def __unicode__(self):
        return u"{L: %f} {T: %f}" % (self.L, self.T)


# Plant subclasses
class Arugula(Plant):
    pass


class EnglishIvy(Plant):
    pass

