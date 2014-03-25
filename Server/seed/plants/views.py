from django.shortcuts import render
from django import forms
import algo.datawrapper as dw
import plants.models 
from django.http import HttpResponse

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
        plant = plants.models.Plant.objects.filter(plant_name=plant_name)[0]
        if plant is None:
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
    return render(request,'runalgo.html',{'update_strs': update_strs})

def sync(request):
    pass


arduino_server_ip = 'http://192.168.1.22/'

def index(request):
    patterns     = Pattern.objects.all()
    pattern_list = '<br></br> '.join(pattern.pattern_id for pattern in patterns)
    title        = '<title>Led_298 Index</title>'
    return HttpResponse(title + "<p>These are the available commands: </p>" + pattern_list)


def detail(request, pattern_id):
    pattern_id = pattern_id.upper()
    pattern             = Pattern.objects.get(pattern_id__iexact = pattern_id)
    pattern_description = "NOTHING!"
    title               = '<title>Led_298 ' + pattern_id + ' </title>'
    if pattern:
        pattern_description = pattern.pattern_description
    return HttpResponse(title + "The pattern " + pattern.pattern_id + " does the following: " + pattern_description)

def perform(request, pattern_id):
    title     = '<title>Led_298 ' + pattern_id + ' Perform </title>'
    pattern_id = pattern_id.upper()
    try:
        response_text = requests.get(arduino_server_ip + '$' + pattern_id, timeout = 3).text + "\n is A-okay!"
    except requests.exceptions.RequestException:
        response_text = "SERVER UNAVAILABLE!"

    return HttpResponse(title + "Querying arduino for pattern " + pattern_id + " yields: " + response_text)


