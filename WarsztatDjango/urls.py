"""
URL configuration for WarsztatDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from reservation_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/new/', views.AddRoom.as_view(), name='add_room'),
    path('room/available/', views.ViewAvailableRooms.as_view(), name='available_rooms'),
    path('room/delete/<int:id>/', views.DeleteRoom.as_view(), name='delete_room'),
    path('room/modify/<int:id>/', views.ModifyRoom.as_view(), name='modify_room'),
    path('room/reserve/<int:id>/', views.ReserveRoom.as_view(), name='reserve_room'),
    path('room/view_room/<int:id>/', views.RoomView.as_view(), name='view_room'),
    path('room/search/', views.RoomSearch.as_view(), name='search_room'),
]
