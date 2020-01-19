from django.urls import path
from . import views


app_name = 'dailyreport'
urlpatterns = [
    path('', views.MyReportView.as_view(), name='dailyreport'),
    path('dailyreport/', views.MyCalendarView.as_view(), name='dailyreport'),
    # path('dailyreport/list/', views.EventListView.as_view(), name='dailyreport-list'),
    # path('dailyreport/create/', views.EventCreateView.as_view(), name='dailyreport-create'),

]
