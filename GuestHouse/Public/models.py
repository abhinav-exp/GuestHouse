from django.db import models
from Organiser.models import Event

# Create your models here.

class Student(models.Model):
    First_Name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    Attending = models.ManyToManyField(Event)
    Start_date = models.DateField()
    End_date = models.DateField()
    Femaleness = models.BooleanField()
    Mobile = models.BigIntegerField()
    Email = models.EmailField()

    def __str__(self):

        def gender(b):
            if b:
                return "Female"
            else:
                return "Male"

        s = "{} {} Start_date {} End_date {} {} {} {}".format(self.First_Name, self.Last_name,
            self.Start_date, self.End_date,
            gender(self.Femaleness), self.Mobile, self.Email)

        return s

class Staff(models.Model):
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=20)
    Name = models.CharField(max_length=30, default="notset")

    def __str__(self):
        s = "{} Password {} Name {}".format(self.Username, self.Password, self.Name)
        return s