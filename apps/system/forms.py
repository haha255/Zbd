from django import forms
from .models import Structure, UserProfile, Role, Menu
from django.contrib.auth import get_user_model
import re


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'requeired': '请填写用户名'})
    password = forms.CharField(required=True, error_messages={'requeired': '请填写密码'})


class StructureForm(forms.ModelForm):
    class Meta:
        model = Structure
        fields = ['type', 'name', 'parent']


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'birthday', 'gender', 'mobile', 'tel']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'desc', 'permissions']


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度最小6位',
            'max_length': '密码长度不能超过20位',
        }
    )
    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度最小6位',
            'max_length': '密码长度不能超过20位',
        }
    )

    class Meta:
        model = User
        fields = [
            'name', 'gender', 'birthday', 'username', 'mobile', 'tel',
            'department', 'post', 'superior', 'roles', 'password'
        ]
        error_messages = {
            'name': {'required': '姓名不能为空'},
            'username': {'required': '用户名不能为空'},
            'mobile': {
                'required': '手机号码不能为空',
                'min_length': '请输入有效手机号码',
                'max_length': '请输入有效手机号码',
            },
        }

        def clean(self):
            cleaned_data = super(UserCreateForm, self).clean()
            username = cleaned_data.get('username')
            mobile = cleaned_data.get('mobile', '')
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if User.objects.filter(username=username).count():
                raise forms.ValidationError('用户名:{}已存在'.format(username))

            if password != confirm_password:
                raise forms.ValidationError('两次密码输入不一致')

            if User.objects.filter(mobile=mobile).count():
                raise forms.ValidationError('手机号码：{}已存在'.format(mobile))

            REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$"
            if not re.match(REGEX_MOBILE, mobile):
                raise forms.ValidationError('手机号码：{}格式非法'.format(mobile))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name', 'gender', 'birthday', 'username', 'mobile', 'tel',
            'department', 'post', 'superior', 'is_active', 'roles'
        ]


class PasswordChangeForm(forms.Form):

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            'required': u'密码不能为空'
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            'required': u'密码不能为空'
        })

    def clean(self):  # 验证通过，重写了祖先对象的clean方法进行额外验证
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('两次密码输入不一致！')


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
