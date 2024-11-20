from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from users.forms import UserLoginForm, UserCreationForm


class UserloginView(LoginView):
    template_name = 'registration/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserRegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('blog:index'))
