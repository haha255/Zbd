from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from .forms import LoginForm, UserCreateForm, UserUpdateForm, PasswordChangeForm
from .mixin import LoginRequiredMixin
from .models import Structure, Role
import re
from django.contrib.auth.hashers import make_password
from django.db.models import Q


User = get_user_model()


class IndexView(LoginRequiredMixin, View):
    """主界面"""
    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    """登录类"""
    def get(self, request):  # get方法
        if not request.user.is_authenticated:
            return render(request, 'system/users/login.html')
        else:
            return HttpResponseRedirect('/')  # 如果已经认证，则回到根页面

    def post(self, request):  # post方法
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活!'
            else:
                ret['msg'] = '用户名或者密码错误!'
        else:
            ret['msg'] = '用户名和密码均不能为空!'
        return render(request, 'system/users/login.html', ret)


class LogoutView(View):
    """注销用户使用"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))  # 反向去找login的URL


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'system/users/user.html'


class UserListView(LoginRequiredMixin, View):

    def get(self, request):
        fields = ['id', 'name', 'gender', 'mobile', 'tel', 'department__name', 'post', 'superior__name', 'is_active']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['is_active'] = request.GET['select']
        ret = dict(data=list(User.objects.filter(**filters).values(*fields)))
        return JsonResponse(ret)


class UserCreateView(LoginRequiredMixin, View):

    def get(self, request):
        users = User.objects.exclude(username='admin')  # 保护admin用户不被修改
        structure = Structure.objects.values()
        roles = Role.objects.values()
        ret = {
            'users': users,
            'structure': structure,
            'roles': roles,
        }
        return render(request, 'system/users/user_create.html', ret)

    def post(self, request):
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)  # 不提交
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            new_user.save()
            user_create_form.save_m2m()  # 存储多对多关系表。
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }
        return JsonResponse(ret)


class UserDetailView(LoginRequiredMixin, View):

    def get(self, request):
        user = get_object_or_404(User, pk=int(request.GET['id']))
        users = User.objects.exclude(Q(id=int(request.GET['id']))
                                     | Q(username='admin'))  # 可以当上级的人
        structures = Structure.objects.values()
        roles = Role.objects.values()
        user_roles = user.roles.values()
        ret = {
            'user': user,
            'structures': structures,
            'users': users,
            'roles': roles,
            'user_roles': user_roles,
        }
        return render(request, 'system/users/user_detail.html', ret)


class UserUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
        else:
            user = get_object_or_404(User, pk=int(request.user.id))
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {'status': 'success'}
        else:
            ret = {'status': 'fail', 'message': user_update_form.errors}
        return JsonResponse(ret)


class PasswordChangeView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            user = get_object_or_404(User, pk=int(request.GET['id']))
            ret['user'] = user
        return render(request, 'system/users/passwd_change.html', ret)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                new_password = request.POST['password']
                user.set_password(new_password)
                user.save()
                ret = {'status': 'success'}
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(form.errors)
                password_change_form_errors = re.findall(pattern, errors)
                ret = {
                    'status': 'fail',
                    'password_change_form_errors': password_change_form_errors[0]
                }
        return JsonResponse(ret)


class UserDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))  # 创建id的int型list
            User.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return JsonResponse(ret)


class UserEnableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=False).update(is_active=True)
            ret['result'] = True
        return JsonResponse(ret)


class UserDisableView(LoginRequiredMixin, View):
    """
    禁用用户：单个或者批量禁用
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=True).update(is_active=False)
            ret['result'] = True
        return JsonResponse(ret)
