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
    wrapper.loadFromDB_nutrientUpdate()
    wrapper.updateNutrients()
    wrapper.persistToDB_nutrientUpdate()
    update_strs = wrapper.updateString()
    return render(request, 'runalgo.html',{'update_strs': update_strs})

def sync(request):
    pass




''' Arduino Server Requests!
'''
arduino_server_ip = 'http://192.168.1.147/'

def index(request):
    plant_objs = plants.models.Plant.objects.all()
    plant_list = '<br></br> '.join(plant.user_name + "'s " + 'plant ' + plant.plant_name for plant in plant_objs)
    title      = '<title>Seed Hydroponics Index</title>'
    return HttpResponse(title + "<p>These are the plants: </p>" + plant_list)

def query_arduino(request):
    try:
        response_text = requests.get(arduino_server_ip + '$' + ".45f,.32f,.19f", timeout = 3).text + "\n is A-okay!"
    except requests.exceptions.RequestException:
        response_text = "SERVER UNAVAILABLE!"

    return HttpResponse('Seed Hyroponics: ' + "Querying arduino with updated info " +
                        str(45) + " yields: " + response_text)



