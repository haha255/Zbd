from django.urls import path
from . import views


app_name = 'sometools'
urlpatterns = [
    path('', views.SomeToolsView.as_view(), name='sometools'),
    path('mycalendar/', views.MyCalendarView.as_view(), name='mycalendar'),
    path('mycalendar/list/', views.EventListView.as_view(), name='mycalendar-list'),
    path('mycalendar/create/', views.EventCreateView.as_view(), name='mycalendar-create'),

]
