from django.db import models
import datetime

class Plant(models.Model):
    ''' Plant is a superclass for all different types of plants we end up using
        currently we have boilerplate for:
            - Arugula
            - English Ivy
    '''
    # Plant Metadata
    initial_date     = models.DateTimeField('Birthday')
    initial_date.editable = True
    is_control = models.BooleanField('Is a control plant')

    # User data
    user_name        = models.CharField("User's Name", max_length=20)
    plant_name       = models.CharField("Plant's Name", max_length=20)

    def __unicode__(self):
        return u"%s's plant %s" % (self.user_name, self.plant_name)


class PlantState(models.Model):
    ''' Plant states represent the different parameters we are keeping track of
        Currently we control nutrient flow, and measure ambient light
    '''

    date                = models.DateTimeField('Date-Time', default=datetime.datetime.now)
    date.editable = True

    timestep            = models.IntegerField('Timestep')
    nutrient_value      = models.FloatField('Nutrient Value', default=0.0)
    light_value         = models.FloatField('Light Value', default=0.0)
    performance_value   = models.FloatField('Performance Value', default=0.0)
    plant               = models.ForeignKey(Plant,related_name='plant_states')

    def __unicode__(self):
        return u"%s's plant %s's state at time step %d" % (self.plant.user_name, self.plant.plant_name, self.timestep)

class ControlPlantState(models.Model):
    date                = models.DateTimeField('Date-Time', auto_now=True)
    date.editable = True

    timestep            = models.IntegerField('Timestep')
    performance_value   = models.FloatField('Performance Value', default=0.0)
    plant               = models.ForeignKey(Plant)

    def __unicode__(self):
        return u"%s's control plant %s's state at time step %d" % (self.plant.user_name, self.plant.plant_name, self.timestep)    

class AlgoMetadata(models.Model):
    ''' Metadata for current state/iteration of algorithm. Contains two variables:
        - Lipschitz constant of performance function
        - Expected time of convergence
    '''
    date      = models.DateTimeField('Date-Time', auto_now=True)
    date.editable = True

    L         = models.FloatField('Lipschitz Constant')
    T         = models.IntegerField('Time of Convergence')
    tau       = models.IntegerField('Time Memory')

    def __unicode__(self):
        return u"{L: %f} {T: %f}" % (self.L, self.T)

class CareConstants(models.Model):
    water_cycle_period = models.FloatField('Water cycle period')
    light_start_hour = models.IntegerField('Light start hour')
    light_end_hour = models.IntegerField('Light end hour')
    def __unicode__(self):
        return u"{Water cycle period: %f} {Light start hour: %i} {Light end hour: %i" % (self.water_cycle_period, self.light_start_hour, self.light_end_hour)

# Plant subclasses
class Arugula(Plant):
    pass


class EnglishIvy(Plant):
    pass

