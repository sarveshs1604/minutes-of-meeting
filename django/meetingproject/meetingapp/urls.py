from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('meeting', views.meeting, name='meeting'),
    path('meetingsave/', views.meetingsave, name='meetingsave'),  # URL for saving meeting details and sending email
    path('meetingsend/<int:id>/', views.meetingsend, name='meetingsend'),
    path('', views.meeting_list,name='meeting_list'),
    path('after_meeting/<int:id>/', views.after_meeting, name='after_meeting'),
    path('points_discussed/<int:id>/', views.points_discussed, name='points_discussed'),
    path('delete_meeting/<int:id>/', views.delete_meeting, name='delete_meeting'),
    path('minutes/<int:id>/', views.minutes_of_meeting, name='minutes_of_meeting'),
    path('assign_tasks/<int:id>/', views.points_agreed, name='points_agreed'),
    path('send_mom/<int:id>/', views.send_mom, name='send_mom'),

 # Example for listing saved meetings (optional)
]
