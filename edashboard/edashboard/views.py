from django.shortcuts import render
from http.server import BaseHTTPRequestHandler, HTTPServer
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.template import Template, Context
from django import template
from edashboard.clean import *
from edashboard.GetBuilding import *
from edashboard.models import ExportBuilding,Demo
from django.views import View
from edashboard.forms import ExportForm
from django.http import JsonResponse
import json
import time

register = template.Library()


def index(request):
    return render(request, 'edashboard/index.html')

def building_view(request):
    return render(request, 'edashboard/building.html')

def compare_view(request):
    return render(request, 'edashboard/compare.html')

class ExportView(View):
    date=[]
    value=[]
    def get(self, request):
        date=[]
        value=[]
        return render(request, 'edashboard/export.html',{'db_data':0, 'db_id':0})

    def post(self, request):
        if request.is_ajax():
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            #Gets start and end times
            timestr = body['time']
            times = timestr.split(" - ")
            #Creates our variables needed for graphing
            timestart = getTimes(times[0])
            timeend = getTimes(times[1])
            building = body['building']
            util = body['util']
            sensor = body['sensor']
            usage = ExportBuilding.objects.filter(date__gte=timestart, date__lte=timeend).values('usage')
            date = ExportBuilding.objects.filter(date__gte=timestart, date__lte=timeend).values('date')
            #usage = ExportBuilding.objects.filter(date__gte=timestart, date__lte=timeend).values('usage','date')
            for i in date:
                if (i.get('date') is not None):
                    i=(str(i.get('date')).split("+")[0]).encode('utf-8')
        return render(request, 'edashboard/export.html',{'date':date, 'usage':usage})

def get_data(request):
    date = "Tues"
    usage = 10
    return JsonResponse({'data': usage,'date':date})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

def compare_view(request):
    db_data = Demo.objects.all().values_list('value', flat=True)
    db_date = Demo.objects.all().values_list('date', flat=True)
    db_id = Demo.objects.all().values_list('id', flat=True)
    print(db_id)
    return render(request, 'edashboard/compare.html',{'db_data':db_data, 'db_id':db_id})

def help_view(request):
    return render(request, 'edashboard/help.html')

def construction_view(request):
    return render(request, 'edashboard/construction.html')

def login_view(request):
    return render(request, 'edashboard/login.html')

def admin_view(request):
    return render(request, 'edashboard/admin.html')
'''
def data(request):
    db_data = Demo.objects.all().values_list('value', flat=True)
    db_date = Demo.objects.all().values_list('date', flat=True)
    return TemplateResponse(request, 'edashboard/export.html', {"db_data" : db_data})

def data_com(request):
    db_data = Demo.objects.all().values_list('value', flat=True)
    db_date = Demo.objects.all().values_list('date', flat=True)
    return TemplateResponse(request, 'edashboard/compare.html', {"db_data" : db_data})

@register.building_name
def getBuildingsName():
    building = []
    filename="buildings.csv"
    with open(filename,'r') as f:
        lines= f.readlines()
        for line in lines:
            if "number,name" not in line:
                building.insert(len(building),line.rsplit(',', 1)[1])
    f.close()
    return building

@register.building_num
def getBuildingsNumber():
    building = []
    filename="buildings.csv"
    with open(filename,'r') as f:
        lines= f.readlines()
        for line in lines:
            if "number,name" not in line:
                building.insert(len(building),line.rsplit(',', 1)[0])
    f.close()
    return building

    FOR REFERENCE LATER
    #Pass in value and convert to kwH and convert based on string that conversion is.
    #CONVERSION LINK https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
    def greenComp(value,conversion):

        kwh = value
        mtons = value*.0007
        kilog=value*0.707
        lbs=value*1.6
        #BARRELS OF OIL 5.80 mmbtu/barrel × 20.31 kg C/mmbtu × 44 kg CO2/12 kg C × 1 metric ton/1,000 kg
        if conversion=="oil":
            return mtons/.43
        #TREE'S GROWN FOR 10 YEARS
        elif conversion=="tree":
            return mtons/.06
        #CARBON OFFSET
        elif conversion=="carbon" :
            return value
        #Converts to Tons
        elif conversion=="tons" :
            return value*.0008
        # Converts to Gas
        elif conversion=="gas" :
            return mtons/(8.887*(10 ** (-3)))
        # CONVERTS BTU TO kWh
        elif conversion=="btu" :
            return kwh * 3412.14
        # Converts to DOLLARS
        else:
            return kwh * 11.1
    '''
