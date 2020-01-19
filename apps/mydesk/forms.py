from django import forms
from .models import DailyReport


class EventCreateForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        min_length=2,
        max_length=1000,
        error_messages={
            'required': '日程不能为空',
            'min_length': '日程长度最小2个字符',
            'max_length': '日程长度不能超过1000个字符',
        }
    )

    class Meta:
        model = DailyReport
        fields = ['title', 'type', 'start', 'end', 'allday', 'participants', 'user']
        error_messages = {
            'start': {'required': '开始时间不能为空'},

        }

    def clean(self):
        cleaned_data = super(EventCreateForm, self).clean()
        start_time = cleaned_data.get('start')
        end_time = cleaned_data.get('end')
        if end_time < start_time:
            raise forms.ValidationError('结束时间应不小于开始时间！')
