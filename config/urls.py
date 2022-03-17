"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from config import settings
from vacancies import views as vacancies_views, error_handlers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vacancies_views.MainView.as_view(), name='home'),
    path('', include('accounts.urls')),
    path('vacancies/', include('vacancies.urls')),
    path('companies/<int:pk>', vacancies_views.CompanyCard.as_view(), name='company_pk'),
    path('mycompany/', vacancies_views.MyCompanyFill.as_view()),
    path('mycompany/vacancies/', vacancies_views.MyCompanyVacancies.as_view()),
    path('mycompany/vacancies/<int:pk>', vacancies_views.MyCompanyVacancyFill.as_view()),


    path('test/', vacancies_views.test, name='test'),
    path('test/<int:pk>/<str:name>', vacancies_views.test, name='test_with_variables'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#     path('login/', vacancies_views.MyLoginView.as_view(), name='login'),
#     path('registration/', vacancies_views.registration.as_view(), name='reg'),
# ]
handler500 = error_handlers.custom_handler500
handler404 = error_handlers.custom_handler404
