from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.http import HttpResponse


class MainView(TemplateView):
    template_name = 'vacancies/index.html'



class AllVacancies(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'Здесь будут все вакансии списком')


class VacanciesByCategory(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'Здесь будут вакансии по категориям')


class CompanyCard(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'Здесь будет карточка компании')


class Vacancy(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'Здесь будет карточка компании')