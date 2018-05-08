from django.urls import path
from rift_missions.views import Homeview
from . import views


app_name = 'rift_missions'

urlpatterns = [
    #path(^$'', views.index, name='index'),
    path('', Homeview.as_view(), name='home'),
    path('highscores/', views.highscores, name='highscores'),
    path('mission/', views.missions, name='missions'),
    path('home/', views.home, name='homes'),
]

