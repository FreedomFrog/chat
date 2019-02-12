from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('telerik/<str:room_name>/', views.telerik_room, name='telerik_room'),
]