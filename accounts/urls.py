from django.urls import path

import accounts.views
from vacancies import views as vacancies_views

urlpatterns = [
    path('login/', accounts.views.login_view, name='login'),
    path('registration/', accounts.views.Registration.as_view(), name='registration'),
    path('logout/', accounts.views.Logout.as_view(), name='logout'),

]
