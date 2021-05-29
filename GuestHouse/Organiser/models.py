from django.db import models
from Staff.models import Organiser

# Create your models here.
class Event(models.Model):
    Name = models.CharField(max_length=50)
    Organised = models.ForeignKey(Organiser, on_delete=models.CASCADE)
    Start_date = models.DateField()
    End_date = models.DateField()
    Permitted = models.BooleanField(default=False)
    Students_acc_male = models.IntegerField(default=0)
    Students_acc_female = models.IntegerField(default=0)
    Students_accd_male = models.IntegerField(default=0)
    Students_accd_female = models.IntegerField(default=0)
    Guest_acc = models.IntegerField(default=0)
    Guest_accd = models.IntegerField(default=0)

    class Meta:
        unique_together = (("Name", "Organised"),)

    def __str__(self):
        s0 = "{} Organiser {} Start_date {} End_date {} Permitted {} Student_male {} / {} Student_female {} / {} Guest {} / {}".format(self.Name,
            self.Organised.Username, self.Start_date,self.End_date,self.Permitted, self.Students_accd_male, self.Students_acc_male, 
            self.Students_accd_female, self.Students_acc_female, self.Guest_accd, self.Guest_acc)
        return s0

class Guest(models.Model):
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Attending = models.ForeignKey(Event, on_delete=models.CASCADE)
    Femaleness = models.BooleanField()
    Mobile = models.BigIntegerField()
    Email = models.EmailField()

    class Meta:
        unique_together = (("First_Name", "Last_Name", "Attending"),)

    def __str__(self):

        def gender(b):
            if b:
                return "Female"
            else:
                return "Male"

        s = "{} {} Event {} {} {} {}".format(self.First_Name, self.Last_Name, self.Attending.Name,
            gender(self.Femaleness), self.Mobile, self.Email)

        return s
