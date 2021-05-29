from django.urls import path
from . import views

urlpatterns = [
    path('checkorganisers', views.checkorganisers),
    path('checkstaffs', views.checkstaffs),
    path('contactorganisers', views.contactorganisers),
    path('listevents', views.listevents),
    path('addstudents', views.addstudents),
]