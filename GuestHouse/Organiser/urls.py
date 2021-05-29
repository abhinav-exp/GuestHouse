from django.urls import path
from . import views

urlpatterns = [
    path('addevents', views.addevents),
    path('listevents', views.listevents),
    path('removeevents', views.removeevents),
    path('editevents', views.editevents),

    path('addguests', views.addguests),
    path('listguests', views.listguests),
    path('removeguests', views.removeguests),

    path('liststudents', views.liststudents),
]