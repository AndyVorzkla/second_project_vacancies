from django.urls import path

import accounts.views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', accounts.views.login_view, name='login'),
    path('registration/', accounts.views.Registration.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
