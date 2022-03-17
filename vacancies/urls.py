from django.urls import path
from vacancies import views as vacancies_views

urlpatterns = [
    path('', vacancies_views.AllVacancies.as_view(), name='all_vacancies'),
    path('<int:pk>', vacancies_views.VacancyView.as_view(), name='vacancy_pk'),
    path('<int:pk>/send', vacancies_views.VacancySend.as_view(), name='send_vacancy'),
    path('cat/<str:category_name>', vacancies_views.VacanciesByCategory.as_view(), name='all_vacancies_by_category'),


]

