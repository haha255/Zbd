from django.views.generic import ListView
from .mixin import LoginRequiredMixin
from .models import Menu
from apps.custom import ZbdUpdateView, ZbdCreateView


class MenuCreateView(ZbdCreateView):
    model = Menu
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(ZbdUpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)
