from django.shortcuts import render
from datetime import date
from .models import Event, Guest
from django.http import JsonResponse
from Staff.models import Organiser 
from Public.models import Student

# Create your views here.
def addevents(requests):
    Name = requests.GET['Name']

    Organised = requests.GET['Username']
    Record_Organiser = Organiser.objects.get(Username = Organised)

    try :
        record =  Event.objects.get(Name = Name, Organised = Record_Organiser)
        return JsonResponse({'status':False})

    except :
        Start_date = int(requests.GET['Start_date'])
        Start_month = int(requests.GET['Start_month'])
        Start_year = int(requests.GET['Start_year'])

        Sd = date(Start_year, Start_month, Start_date)

        End_date = int(requests.GET['End_date'])
        End_month = int(requests.GET['End_month'])
        End_year = int(requests.GET['End_year'])

        Ed = date(End_year, End_month, End_date)

        Permitted = False
        Students_acc_male = requests.GET['Students_acc_male']
        Students_acc_female = requests.GET['Students_acc_female']
        Guest_acc = requests.GET['Guest_acc']

        record_Event = Event(Name = Name, 
                            Organised = Record_Organiser, 
                            Start_date = Sd, 
                            End_date = Ed, 
                            Permitted = Permitted,
                            Students_acc_male = Students_acc_male,
                            Students_acc_female = Students_acc_female,
                            Guest_acc = Guest_acc)

        record_Event.save()
        return JsonResponse({'status':True})

def listevents(requests):
    Organised = requests.GET['Username']
    Record_Organiser = Organiser.objects.get(Username = Organised)

    records =  Event.objects.filter(Organised = Record_Organiser)

    data = {}
    data['Events'] = []

    for record in records:
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
        data['Events'].append(rec)

    return JsonResponse(data)

def removeevents(requests):
    Name = requests.GET['Name']
    Username = requests.GET['Username']

    try :
        Record_Organiser = Organiser.objects.get(Username = Username)
        Record = Event.objects.get(Name = Name, Organised = Record_Organiser)
        Record.delete()
        return JsonResponse({'status':True})
    except :
        return JsonResponse({'status':False})

def editevents(requests):
    Name = requests.GET['Name']

    Organised = requests.GET['Username']
    Record_Organiser = Organiser.objects.get(Username = Organised)

    try :
        record =  Event.objects.get(Name = Name, Organised = Record_Organiser)
        try :
            record.Start_date.day = int(requests.GET['Start_date'])
        except :
            pass
        try :
            record.Start_date.month = int(requests.GET['Start_month'])
        except :
            pass
        try :
            record.Start_date.year = int(requests.GET['Start_year'])
        except :
            pass
        try :
            recored.End_date.day = int(requests.GET['End_date'])
        except :
            pass
        try :
            record.End_date.month = int(requests.GET['End_month'])
        except :
            pass
        try :
            record.End_date.year = int(requests.GET['End_year'])
        except :
            pass
        try :
            record.Students_acc_male = requests.GET['Students_acc_male']
        except :
            pass
        try :
            record.Students_acc_female = requests.GET['Students_acc_female']
        except :
            pass
        try :
            Guest_acc = requests.GET['Guest_acc']
        except :
            pass
        Permitted = False
        record.save()
        return JsonResponse({'status':True})

    except :
        return JsonResponse({'status':False})

def addguests(requests):
    try :
        First_Name = requests.GET['First_Name']
        Last_Name = requests.GET['Last_Name']

        Name = requests.GET['Name']
        Organised = Organiser.objects.get(Username = requests.GET['Username'])
        Attending = Event.objects.get(Name = Name, Organised = Organised) 

        Femaleness = bool(requests.GET['Femaleness']=='true')
        Mobile = int(requests.GET['Mobile'])
        Email = requests.GET['Email']

        record = Guest(First_Name = First_Name,
                        Last_Name = Last_Name,
                        Attending = Attending,
                        Femaleness = Femaleness,
                        Mobile = Mobile,
                        Email = Email)
    
        if not record.Attending.Guest_acc > record.Attending.Guest_accd :
            return JsonResponse({'status' : False})

        Attending.Guest_accd = Attending.Guest_accd + 1

        Attending.save()
        record.save()

        return JsonResponse({'status' : True})
    except :
        return JsonResponse({'status' : False})

def listguests(requests):
    Username = requests.GET['Username']
    Organised = Organiser.objects.get(Username = Username)

    Events = Event.objects.filter(Organised = Organised)
    
    data = {}
    data['Guests'] = {}

    for rec_event in Events:
        data['Guests'][rec_event.Name] = []
        for rec_guest in Guest.objects.filter(Attending = rec_event):
            data['Guests'][rec_event.Name].append({'First_Name' : rec_guest.First_Name,
                                                    'Last_Name' : rec_guest.Last_Name, 
                                                    'Femaleness' : rec_guest.Femaleness,
                                                    'Mobile' : rec_guest.Mobile,
                                                    'Email' : rec_guest.Email})

    """for rec_Event in Events:
        for rec_guest in Guest.objects.filter(Attending = rec_Event):
            data['Guests'].append({'First_Name' : rec_guest.First_Name,
                                    'Last_Name' : rec_guest.Last_Name,
                                    'Attending' : rec_guest.Attending.Name, 
                                    'Femaleness' : rec_guest.Femaleness,
                                    'Mobile' : rec_guest.Mobile,
                                    'Email' : rec_guest.Email})"""

    return JsonResponse(data)

def removeguests(requests):
    try :
        Username = requests.GET['Username']
        Organised = Organiser.objects.get(Username = Username)

        Name = requests.GET['Name']
        rec_Event = Event.objects.get(Name = Name, Organised = Organised)

        First_Name = requests.GET['First_Name']
        Last_Name = requests.GET['Last_Name']
        record = Guest.objects.get(First_Name = First_Name, Last_Name = Last_Name, Attending = rec_Event)
        record.delete()
        return JsonResponse({'status' : True})
    except :
        return JsonResponse({'status' : False})

def liststudents(requests):
    Organised = requests.GET['Username']
    Record_Organiser = Organiser.objects.get(Username = Organised)

    Records_Event =  Event.objects.filter(Organised = Record_Organiser)

    data = {}
    data['Events'] = {}

    for record_event in Records_Event:
        data['Events'][record_event.Name] = []

        for record_student in Student.objects.all():
            if record_event in record_student.Attending.all():
                rec = {}
                rec['First_Name'] = record_student.First_Name
                rec['Last_Name'] = record_student.Last_name

                rec['Start_date'] = record_student.Start_date.day
                rec['Start_month'] = record_student.Start_date.month
                rec['Start_year'] = record_student.Start_date.year

                rec['End_date'] = record_student.End_date.day
                rec['End_month'] = record_student.End_date.month
                rec['End_year'] = record_student.End_date.year

                rec['Femaleness'] = record_student.Femaleness
                rec['Mobile'] = record_student.Mobile
                rec['Email'] = record_student.Email

                data['Events'][record_event.Name].append(rec)

    return JsonResponse(data)
