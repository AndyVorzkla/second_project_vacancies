from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from accounts.forms import *
from vacancies.models import *


def login_view(request, *args, **kwargs):
    template_name = 'accounts/login.html'
    if request.method.lower() == 'post':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                # the password verified for the user
                if user.is_active: # User is valid, active and authenticated
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error('username', 'Данный пользователь заблокирован.')
            else:
                # the authentication system was unable to verify the username and password
                form.add_error('password', 'Неправильный логин или пароль')
            # try:
            #     user = User.objects.get(username=data['username'])
            #     if user.check_password(data['password']):
            #         request.user = user
            #         print(request.user)
            #         return redirect('home')
            #     else:
            #         form.add_error('password', 'Проверьте правильность пароля.')
            # except User.DoesNotExist:
            #     form.add_error('username', 'Данного пользователя не существует.')
    else:
        form = SignUpForm()

    return render(request, template_name, context={'form': form})


class Registration(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, template_name=self.template_name, context={'form': RegistrationForm})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.get(username=data['username'])
                form.add_error('username', 'Данный логин уже используется')
            except User.DoesNotExist:
                User.objects.create_user(**data)
                return redirect('login')
        return render(request, template_name=self.template_name, context={'form': form})


class Logout(TemplateView):
    template_name = ''
