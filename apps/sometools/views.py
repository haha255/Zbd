from django.views.generic.base import TemplateView, View
from apps.system.mixin import LoginRequiredMixin
from .models import Calendar, Dic_Event_Type
from .forms import EventCreateForm
from django.http import JsonResponse
from django.shortcuts import render
import datetime
import re


class SomeToolsView(LoginRequiredMixin, TemplateView):

    template_name = 'system/system_index.html'


class MyCalendarView(LoginRequiredMixin, TemplateView):

    template_name = 'sometools/mycalendar.html'


class EventListView(LoginRequiredMixin, View):

    def post(self, request):
        # get方法取得日历事件
        fields = ['id', 'type', 'title', 'start', 'end', 'allday', 'isfinish', 'type__color']
        start = end = None
        if 'start' in request.POST and request.POST['start']:
            start = datetime.datetime.strptime(request.POST['start'], '%Y-%m-%dT%H:%M:%S')
        if 'end' in request.POST and request.POST['end']:
            end = datetime.datetime.strptime(request.POST['end'], '%Y-%m-%dT%H:%M:%S')
        if start and end:
            qs = Calendar.objects.filter(start__gte=start).filter(end__lte=end).values(*fields)
        elif start:
            qs = Calendar.objects.filter(start__gte=start).values(*fields)
        elif end:
            qs = Calendar.objects.filter(end__lte=end).values(*fields)
        else:
            qs = Calendar.objects.values(*fields)
        ret = dict(data=list(qs))  # 传一个列表，用于取得想要的字段
        return JsonResponse(ret)


class EventCreateView(LoginRequiredMixin, View):

    def get(self, request):
        types = Dic_Event_Type.objects.all()
        start = end = None
        if 'start' in request.GET and request.GET['start']:
            start = request.GET['start']
            start = ' '.join(start.split('T'))  # 目的是为了将'YYYY-MM-DDThh:mm'转换为'YYYY-MM-DD hh:mm'
        if 'end' in request.GET and request.GET['end']:
            end = request.GET['end']
            end = ' '.join(end.split('T'))  # 同start
        ret = {
            'types': types,
            'start': start,
            'end': end
        }
        return render(request, 'sometools/event_create.html', ret)

    def post(self, request):
        event_create_form = EventCreateForm(request.POST)
        if event_create_form.is_valid():
            event_create_form.save()  # 提交
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(event_create_form.errors)
            event_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'event_create_form_errors': event_create_form_errors[0]
            }
        return JsonResponse(ret)
