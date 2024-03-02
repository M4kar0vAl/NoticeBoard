from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .filters import ResponseFilter, AdvertFilter
from .forms import AdvertForm, ResponseForm
from .models import *


class AdvertList(ListView):
    model = Advert
    template_name = 'board/adverts.html'
    context_object_name = 'adverts'
    ordering = '-created'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.path == reverse('user_advert_list'):
            queryset = queryset.filter(user=self.request.user)
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'board/advert.html'
    context_object_name = 'advert'

    def get_object(self, queryset=None):
        obj = cache.get(f'advert-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object()
            cache.set(f'advert-{self.kwargs["pk"]}', obj)
        return obj


class AdvertCreate(LoginRequiredMixin, CreateView):
    model = Advert
    form_class = AdvertForm
    template_name = 'board/advert_create.html'

    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.user = self.request.user
        return super().form_valid(form)


class AdvertEdit(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_advert',)
    model = Advert
    form_class = AdvertForm
    template_name = 'board/advert_edit.html'

    def test_func(self):
        if self.request.user == self.get_object().user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

    def form_valid(self, form):
        advert = form.save(commit=True)
        cache.delete(f'advert-{advert.pk}')
        return super().form_valid(form)

class AdvertDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_advert',)
    model = Advert
    template_name = 'board/advert_delete.html'
    success_url = reverse_lazy('advert_list')

    def test_func(self):
        if self.request.user == self.get_object().user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_create.html'
    success_url = reverse_lazy('advert_list')

    def form_valid(self, form):
        response = form.save(commit=False)
        advert = Advert.objects.get(pk=self.request.GET.get('advert_pk'))
        response.advert = advert
        response.user = self.request.user
        if response.advert.user == response.user:
            form.add_error(None, _('You cannot respond to your own advertisements'))
            return self.form_invalid(form)
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/responses.html'
    context_object_name = 'responses'
    ordering = '-created'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(advert__user=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect
def response_action_handle(request):
    if request.method == 'POST':
        response_pk = request.POST.get('response_pk')
        response_obj = Response.objects.get(pk=response_pk)
        action = request.POST.get('action')

        if action == 'accept':
            response_obj.accept()
        elif action == 'reject':
            response_obj.reject()
    return redirect('response_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        category = request.POST.get('category')
        action = request.POST.get('action')
        if action == 'subscribe':
            user.subscriptions.append(category)
            user.save()
        elif action == 'unsubscribe':
            user.subscriptions.remove(category)
            user.save()
        elif action == 'clear':
            user.subscriptions.clear()
            user.save()
        elif action == 'all':
            user.subscriptions = [cat[0] for cat in Advert.CATEGORY_CHOICES[1:]]
            user.save()
        return redirect('subscriptions')
    categories = Advert.CATEGORY_CHOICES[1:]
    return render(request, 'board/subscriptions.html', context={'categories': categories})
