from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from rest_framework import generics, permissions

from oauth2_provider.models import AccessToken

from users.forms import UserEditForm, UserRegisterForm, UserDeleteForm
from users.models import User, UserRole
from users.serializers import UserSerializer


class AdminPermissionsMixin:
    permissions_exception = PermissionDenied(
        'Only user with admin role can delete other users.'
    )

    def check_permissions(self):
        if self.request.user.role != UserRole.ADMIN:
            raise self.permissions_exception

    def get(self, *args, **kwargs):
        self.check_permissions()
        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_permissions()
        return super().post(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse('users:login')

    def form_valid(self, form):
        form.save()

        # TODO: publish event
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'users/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(users=User.objects.all())
        return context


class UserDeleteView(LoginRequiredMixin, AdminPermissionsMixin, FormView):
    form_class = UserDeleteForm
    template_name = 'users/delete.html'

    def get_success_url(self):
        return reverse('users:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        delete_user = get_object_or_404(User, id=form.cleaned_data['user_id'])
        delete_user.delete()

        # TODO: publish event
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_id=self.kwargs['user_id'])
        return context


class UserEditView(LoginRequiredMixin, AdminPermissionsMixin, FormView):
    form_class = UserEditForm
    template_name = 'users/edit.html'

    def get_success_url(self):
        return reverse('users:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(instance=get_object_or_404(User, id=self.kwargs['user_id']))
        return kwargs

    def form_valid(self, form):
        form.save()

        # TODO: publish event
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(role_choices=UserRole.choices)
        return context


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @staticmethod
    def get_authorization_token(request):
        token = request.headers.get('Authorization', '')
        if token:
            token = token.lstrip('Bearer ')
        return token

    def get_object(self):
        token = self.get_authorization_token(self.request)
        print(token)
        user = User.objects.get(oauth2_provider_accesstoken__token=token)
        print(user)
        return user
