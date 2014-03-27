from django.shortcuts import render
from django import forms
from django.http import HttpResponse

import requests
import algo.datawrapper as dw
import plants.models


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
    plant_objs = plants.models.Plant.objects.all()
    plant_list = '<br></br> '.join(plant.user_name + "'s " + 'plant ' + plant.plant_name for plant in plant_objs)
    title      = '<title>Seed Hydroponics Index</title>'
    return HttpResponse(title + "<p>These are the plants: </p>" + plant_list)

def sync(request):
    wrapper = dw.DataWrapper()
    wrapper.loadFromDB_performanceUpdate()
    new_values = wrapper.N_t
    # Assume we have 4 plants with names plant0,plant1,plant2,plant3 and submit updates in that order
    # Use ugly hard-coded for-loop to order new_values to reflect this assumption
    new_values_ordered = [0,0,0,0]
    for i in range(0, wrapper.n):
        if wrapper.plantIndexMap[i].plant_name=='plant0':
            new_values_ordered[0] = new_values[i]
        elif wrapper.plantIndexMap[i].plant_name=='plant1':
            new_values_ordered[1] = new_values[i]
        elif wrapper.plantIndexMap[i].plant_name=='plant2':
            new_values_ordered[2] = new_values[i]
        elif wrapper.plantIndexMap[i].plant_name=='plant3':
            new_values_ordered[3] = new_values[i]

    new_values_str = ",".join([str(v).strip('[] ')+ "f" for v in new_values_ordered])
    return HttpResponse('$' + new_values_str + '$')



