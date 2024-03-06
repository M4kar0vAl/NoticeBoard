from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
        # if requested page is list of current user's adverts, then filter all adverts by current user,
        # show all otherwise
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
        # get advert from cache
        obj = cache.get(f'advert-{self.kwargs["pk"]}', None)

        # if advert was not in cache, then get it from db and add to cache
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
        """
        If current user is author of the advert, then allow him to edit it
        If current user has permissions to edit adverts, then allow it
        Prohibit otherwise
        """
        if self.request.user == self.get_object().user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

    def form_valid(self, form):
        advert = form.save(commit=True)
        # delete advert from cache when it was edited
        cache.delete(f'advert-{advert.pk}')
        return super().form_valid(form)


class AdvertDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_advert',)
    model = Advert
    template_name = 'board/advert_delete.html'
    success_url = reverse_lazy('advert_list')

    def test_func(self):
        """
        If current user is author of the advert, then allow him to delete it
        If current user has permissions to delete adverts, then allow it
        Prohibit otherwise
        """
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
        # if current user is author of the advert, which he tries to respond to,
        # then add non-field error to form and make it invalid
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
        # if request came from "responses to user's adverts" page, then show all responses to user's adverts
        if self.request.path == reverse('response_list'):
            queryset = queryset.filter(advert__user=self.request.user)
        # if request came from "user's responses" page, then show responses created by current user
        elif self.request.path == reverse('user_response_list'):
            queryset = queryset.filter(user=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'board/response.html'
    context_object_name = 'response'


class ResponseEdit(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_response',)
    model = Response
    template_name = 'board/response_edit.html'
    form_class = ResponseForm

    def test_func(self):
        """
        If response is accepted, then prohibit to edit it.
        If not accepted:
            allow to edit if current user is author of the response
            allow to edit if current user has permission to edit responses
            prohibit otherwise
        """
        if self.get_object().is_accepted:
            return False
        if self.request.user == self.get_object().user:
            self.permission_required = ()
            return True
        if self.request.user.has_perms(self.permission_required):
            return True
        return False


class ResponseDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_response',)
    model = Response
    template_name = 'board/response_delete.html'
    success_url = reverse_lazy('user_response_list')

    def test_func(self):
        """
        If current user is author, then allow to delete response.
        If current user has permission to delete responses, then allow to delete it.
        Prohibit otherwise
        """
        if self.request.user == self.get_object().user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False


@login_required
@csrf_protect
def response_action_handle(request):
    """
    View that handles accept and reject methods of response.
    """
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
    """
    View that handles subscriptions.
    If request method is GET, then show list of all categories and buttons "subscribe" and "unsubscribe".
    If request method is POST, then get current user, category and action.
    Action can be one of the following: 'subscribe', 'unsubscribe', 'clear', 'all'.
        'subscribe' - subscribes user to category,
        'unsubscribe' - unsubscribes user from category,
        'clear' - unsubscribes user from all categories,
        'all' - subscribes user to all categories.
    After action is handled redirects user to subscriptions page.
    """
    if request.method == 'POST':
        user = request.user
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
