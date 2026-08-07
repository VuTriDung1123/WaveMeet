from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('room/create/', views.create_room, name='create_room'),
    path('room/join/', views.join_room, name='join_room'),
    path('room/<uuid:room_id>/', views.room_detail, name='room_detail'),
    path('room/<uuid:room_id>/lock/', views.toggle_room_lock, name='toggle_room_lock'),
]
