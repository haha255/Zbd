from django import forms
from .models import Dic_Event_Type, Calendar


class EventCreateForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        min_length=2,
        max_length=60,
        error_messages={
            'required': '日程不能为空',
            'min_length': '日程长度最小2个字符',
            'max_length': '日程长度不能超过60个字符',
        }
    )

    class Meta:
        model = Calendar
        fields = ['title', 'type', 'start', 'end', 'allday']
        error_messages = {
            'start': {'required': '开始时间不能为空'},

        }
