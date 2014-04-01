from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.core import serializers
import datetime
import algo.datawrapper as dw
import plants.models
import json


class UpdateForm(forms.Form):
    plant_name = forms.CharField(max_length=100)
    new_value = forms.CharField()
    def is_valid(self):
        valid = super(UpdateForm, self).is_valid()
        if not valid:
            return valid
        plant_name = self.cleaned_data['plant_name']
        new_value = self.cleaned_data['new_value']
        try:
            p = float(new_value)
        except ValueError:
            return False
        if len(plants.models.Plant.objects.filter(plant_name=plant_name))==0:
            return False
        return True


def update_performance(request):
    message = ""
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            plant_name = form.cleaned_data['plant_name']
            new_value = form.cleaned_data['new_value']
            p = float(new_value)
            plant = plants.models.Plant.objects.filter(plant_name=plant_name)[0]
            wrapper = dw.DataWrapper()
            wrapper.loadFromDB_performanceUpdate()
            wrapper.updatePerformance(plant,p)
            wrapper.persistToDB_performanceUpdate()
            message = "Successfully updated plant "+plant.plant_name+" with value "+str(p)
        else:
            message = "Error"
    else:
        form = UpdateForm() # An unbound form

    return render(request, 'update.html', {
        'form': form,
        'message': message
    })

def update_nutrients(request):
    wrapper = dw.DataWrapper()
    update_strs = ""
    msg = ""
    if wrapper.loadFromDB_nutrientUpdate():
        wrapper.updateNutrients()
        wrapper.persistToDB_nutrientUpdate()
        update_strs = wrapper.updateString()
    else:
        msg = "Did not update every value!"
    return render(request, 'runalgo.html', {'update_strs': update_strs, 'msg': msg})

''' Arduino Server Requests!
'''

arduino_server_ip = 'http://192.168.1.147/'


def index(request):
    # Get list of all control states
    plant_states     = plants.models.PlantState.objects.all()
    plant_objs       = plants.models.Plant.objects.all()
    hist_plant_dict  = {}
    donut_plant_dict = {}

    # iterate through plants
    for plant_obj in plant_objs:

        # Create histogram data
        state_list = plant_states.filter(plant=plant_obj)
        hist_plant_dict[plant_obj.plant_name.encode('utf8')] = json.loads(serializers.serialize('json', state_list))

        if not plant_obj.is_control:
        # Create donut data
            recent_states = plant_states.filter(plant=plant_obj).latest('timestep')
            donut_plant_dict[plant_obj.plant_name.encode('utf8')] = json.loads(serializers.serialize('json', [recent_states]))



    hist_dict_str  = json.dumps(hist_plant_dict)
    donut_dict_str = json.dumps(donut_plant_dict)
    return render(request, 'index.html', {'hist_plant_dict': hist_dict_str, 'donut_plant_dict': donut_dict_str})

def sync(request):
    wrapper = dw.DataWrapper()
    wrapper.loadFromDB_performanceUpdate()
    duty_cycles = wrapper.N_t
    care = plants.models.CareConstants.objects.latest('water_cycle_period')
    water_cycle_period = care.water_cycle_period
    light_start_hour = care.light_start_hour
    light_end_hour = care.light_end_hour
    # Assume we have 4 plants with names plant0,plant1,plant2,plant3 and submit updates in that order
    # Use ugly hard-coded for-loop to order duty_cycles to reflect this assumption
    care_values_ordered = [0,0,0,0,0]
    now = datetime.datetime.now()
    for i in range(0, wrapper.n):
        plant = wrapper.plantIndexMap[i]
        timedel = now-plant.initial_date
        seconds = timedel.total_seconds()
        if plant.plant_name == 'plant0':
            if seconds%water_cycle_period <= duty_cycles[i]*water_cycle_period:
                care_values_ordered[0] = 1
        elif plant.plant_name=='plant1':
            if seconds%water_cycle_period <= duty_cycles[i]*water_cycle_period:
                care_values_ordered[1] = 1
        elif plant.plant_name=='plant2':
            if seconds%water_cycle_period <= duty_cycles[i]*water_cycle_period:
                care_values_ordered[2] = 1
        elif plant.plant_name=='plant3':
            if seconds%water_cycle_period <= duty_cycles[i]*water_cycle_period:
                care_values_ordered[3] = 1
    if now.hour >= light_start_hour and now.hour < light_end_hour:
        care_values_ordered[4] = 1

    duty_cycles_str = ",".join([str(v).strip('[] ')+ "f" for v in care_values_ordered])
    return HttpResponse('$' + duty_cycles_str + '$')

def stream(request):
    return render(request, 'stream.html', {})

def analytics(request):
    return render(request, 'analytics.html', {})