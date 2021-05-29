from django.shortcuts import render
from .models import Organiser
from django.http import JsonResponse
from Organiser.models import Event, Guest
from Public.models import Student

# Create your views here.
def addorganisers(requests):
    Username = requests.GET['Username']
    try :
        record = Organiser.objects.get(Username = Username)
        return JsonResponse({'status':False})
    except :
        Category = requests.GET['Category']
        Password = requests.GET['Password']
        Mobile = requests.GET['Mobile']
        Email = requests.GET['Email']
        record = Organiser(Username = Username,
                        Category = Category,
                        Password = Password,
                        Mobile = Mobile,
                        Email = Email)
        record.save()
        return JsonResponse({'status':True})

def listorganisers(requests):
    data = {}
    data['Organisers'] = []
    for record in Organiser.objects.all():
        data['Organisers'].append({'Username':record.Username, 
                                'Category':record.Category,
                                'Mobile':record.Mobile,
                                'Email':record.Email,})
    return JsonResponse(data)

def removeorganisers(requests):
    Username = requests.GET['Username']
    try :
        record = Organiser.objects.get(Username = Username)
        record.delete()
        return JsonResponse({'status':True})
    except :
        return JsonResponse({'status':False})

def listevents(requests):
    data = {}
    data['Events'] = []

    for record in Event.objects.all() :
        rec = {}
        rec['Name'] = record.Name
        rec['Organised'] = record.Organised.Username
        rec['Start_date'] = record.Start_date.day
        rec['Start_month'] = record.Start_date.month
        rec['Start_year'] = record.Start_date.year
        rec['End_date'] = record.End_date.day
        rec['End_month'] = record.End_date.month
        rec['End_year'] = record.End_date.year
        rec['Permitted'] = record.Permitted
        rec['Students_acc_male'] = record.Students_acc_male
        rec['Students_acc_female'] = record.Students_acc_female
        rec['Students_accd_male'] = record.Students_accd_male
        rec['Students_accd_female'] = record.Students_accd_female
        rec['Guest_acc'] = record.Guest_acc
        rec['Guest_accd'] = record.Guest_accd
        rec['Guests'] = []
        for record_guest in Guest.objects.filter(Attending = record):
            rec_guest = {}
            rec_guest['firstName'] = record_guest.First_Name
            rec_guest['lastName'] = record_guest.Last_Name
            rec_guest['femaleness'] = record_guest.Femaleness
            rec_guest['phoneNumber'] = record_guest.Mobile
            rec_guest['email'] = record_guest.Email
            rec['Guests'].append(rec_guest)
        data['Events'].append(rec)

    data['Events'].reverse()
    return JsonResponse(data)

def permitevents(requests):
    try :
        Name = requests.GET['Name']
        Organised = Organiser.objects.get(Username = requests.GET['Username'])
        record = Event.objects.get(Name = Name, Organised = Organised)
        record.Permitted = True
        record.save()
        return JsonResponse({'status':True})
    except :
        return JsonResponse({'status':False})

def liststudents(requests):
    data = {}
    data['Students'] = []

    for record in Student.objects.all():
        rec = {}
        rec['First_Name'] = record.First_Name
        rec['Last_Name'] = record.Last_name
        rec['Attending'] = []

        for record_event in record.Attending.all():
            rec_event = {}
            rec_event['Name'] = record_event.Name
            rec['Attending'].append(rec_event)

        rec['Start_date'] = record.Start_date.day
        rec['Start_month'] = record.Start_date.month
        rec['Start_year'] = record.Start_date.year

        rec['End_date'] = record.End_date.day
        rec['End_month'] = record.End_date.month
        rec['End_year'] = record.End_date.year

        rec['Femaleness'] = record.Femaleness
        rec['Mobile'] = record.Mobile
        rec['Email'] = record.Email

        data['Students'].append(rec)

    return JsonResponse(data)