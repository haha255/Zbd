from django.urls import path
from . import views


app_name = 'mydesk'
urlpatterns = [
    path('', views.MyDeskView.as_view(), name='mydesk'),
    path('dailyreport/', views.MyReportView.as_view(), name='dailyreport'),
    path('dailyreport/create/', views.EventCreateView.as_view(), name='dailyreport-create'),
    path('dailyreport/json/', views.EventListView.as_view(), name='dailyreport-json'),
    path('dailyreport/detail/', views.EventDetailView.as_view(), name='dailyreport-detail'),
    path('dailyreport/test/', views.TestView.as_view(), name='dailyreport-test'),

]
