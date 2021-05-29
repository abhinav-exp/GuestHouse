from django.shortcuts import render
from Staff.models import Organiser
from Organiser.models import Event 
from .models import Student, Staff
from django.http import JsonResponse
from datetime import date
# Create your views here.

def checkorganisers(requests):
    Username = requests.GET['Username']
    try :
        record = Organiser.objects.get(Username = Username)
        Password = requests.GET['Password']
        if Password == record.Password :
            return JsonResponse({'status':True})
        else :
            return JsonResponse({'status':False})
    except :
        return JsonResponse({'status':False})
        
def listevents(requests):
    data = {}
    data['data'] = {}
    data['data']['Events'] = []
    Events = Event.objects.filter(Permitted = True)
    data['dates'] = {}
    Min_Start = Events.earliest('Start_date').Start_date
    data['dates']['Min_Start_date'], data['dates']['Min_Start_month'], data['dates']['Min_Start_year'] \
        = Min_Start.day , Min_Start.month, Min_Start.year
    Max_End = Events.latest('End_date').End_date
    data['dates']['Max_End_date'], data['dates']['Max_End_month'], data['dates']['Max_End_year'] \
        = Max_End.day, Max_End.month, Max_End.year
    for record in  Events:
        if record.Students_acc_male == 0 and record.Students_acc_female == 0:
            continue 
        rec = {}
        rec['Name'] = record.Name
        rec['Organised'] = record.Organised.Username
        rec['Category'] = record.Organised.Category
        rec['Start_date'] = record.Start_date.day
        rec['Start_month'] = record.Start_date.month
        rec['Start_year'] = record.Start_date.year
        rec['End_date'] = record.End_date.day
        rec['End_month'] = record.End_date.month
        rec['End_year'] = record.End_date.year
        #rec['Permitted'] = record.Permitted
        rec['Students_acc_male'] = record.Students_acc_male
        rec['Students_acc_female'] = record.Students_acc_female
        rec['Students_accd_male'] = record.Students_accd_male
        rec['Students_accd_female'] = record.Students_accd_female
        #rec['Guest_acc'] = record.Guest_acc
        #rec['Guest_accd'] = record.Guest_accd
        data['data']['Events'].append(rec)

    return JsonResponse(data)

def contactorganisers(requests):
    Username = requests.GET['Username']
    phone = Organiser.objects.get(Username = Username).Mobile
    return JsonResponse({'Contact':phone})

def addstudents(requests):

    First_Name = requests.GET['First_Name']
    Last_name = requests.GET['Last_Name']
    Attending = requests.GET['Attending']
    Attending_neg = []
    #print("RRRRRRRR")
    Start_date = int(requests.GET['Start_date'])
    Start_month = int(requests.GET['Start_month'])
    Start_year = int(requests.GET['Start_year'])

    Sd = date(Start_year, Start_month, Start_date)

    End_date = int(requests.GET['End_date'])
    End_month = int(requests.GET['End_month'])
    End_year = int(requests.GET['End_year'])

    Ed = date(End_year, End_month, End_date)

    Femaleness = bool(requests.GET['Femaleness']=='true')
    print("Femaleness = "+str(Femaleness))
    Mobile = int(requests.GET['Mobile'])
    Email = requests.GET['Email']

    record = Student(First_Name = First_Name,
                    Last_name = Last_name,
                    Start_date = Sd,
                    End_date = Ed,
                    Femaleness = Femaleness,
                    Mobile = Mobile,
                    Email = Email)
    
    #print(Attending)
    for rec in Attending.split('$$'):
        #print("&&&&&&&")
        #print(rec)

        Username, Name = rec.split('>>')
        Oragnised = Organiser.objects.get(Username = Username)
        rec_event = Event.objects.get(Name = Name, Organised = Oragnised)

        if Femaleness :
            if not rec_event.Students_acc_female > rec_event.Students_accd_female :
                Attending_neg.append(rec)
        else :
            if not rec_event.Students_acc_male > rec_event.Students_accd_male :
                Attending_neg.append(rec)
    
    if len(Attending_neg) :
        return JsonResponse({'status' : False, 'Attending_neg' : Attending_neg})

    record.save()
    for rec in Attending.split('$$') :
        Username, Name = rec.split('>>')
        Oragnised = Organiser.objects.get(Username = Username)
        rec_event = Event.objects.get(Name = Name, Organised = Oragnised)

        if Femaleness :
            rec_event.Students_accd_female = rec_event.Students_accd_female + 1
        else :
            rec_event.Students_accd_male = rec_event.Students_accd_male + 1
        
        record.Attending.add(rec_event)
        rec_event.save()

    record.save()

    return JsonResponse({'status' : True, 'Attending_neg' : []})

def checkstaffs(requests):
    Username = requests.GET['Username']
    try :
        #print("$$$")
        record = Staff.objects.get(Username = Username)
        #print("&&&&")
        Password = requests.GET['Password']
        #print(Password)
        if Password == record.Password :
            return JsonResponse({'status':True, 'Name':record.Name})
        else :
            return JsonResponse({'status':False})
    except :
        return JsonResponse({'status':False})    
