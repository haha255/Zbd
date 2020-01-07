from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from system.mixin import LoginRequiredMixin
from django.http import Http404


class ZbdGetObjectMixin:

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        if 'id' in self.request.GET and self.request.GET['id']:
            queryset = queryset.filter(id=int(self.request.GET['id']))
        elif 'id' in self.request.POST and self.request.POST['id']:
            queryset = queryset.filter(id=int(self.request.POST['id']))
        else:
            raise AttributeError('必须通过id值生成详细视图{}'.format(self.__class__.__name__))
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class ZbdEditViewMixin:

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            res['result'] = True
            form.save()
        return JsonResponse(res)


class ZbdCreateView(LoginRequiredMixin, ZbdEditViewMixin, CreateView):
    """
    view
    """


class ZbdUpdateView(LoginRequiredMixin, ZbdEditViewMixin, ZbdGetObjectMixin, UpdateView):

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)