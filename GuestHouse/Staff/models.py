from django.db import models

# Create your models here.
class Organiser(models.Model):
    Username = models.CharField(max_length=30, primary_key=True)
    Password = models.CharField(max_length=12)
    Category = models.CharField(max_length=30)
    Mobile = models.BigIntegerField()
    Email = models.EmailField()

    def __str__(self):
        s = "{} Password {} Category {} {} {}".format(self.Username,
        self.Password, self.Category, self.Mobile, self.Email)

        return s