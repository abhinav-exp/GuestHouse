from django.urls import path
from . import views

urlpatterns = [
    path('addorganisers', views.addorganisers),
    path('listorganisers', views.listorganisers),
    path('removeorganisers', views.removeorganisers),

    path('listevents', views.listevents),
    path('permitevents', views.permitevents),
    path('liststudents', views.liststudents),
]