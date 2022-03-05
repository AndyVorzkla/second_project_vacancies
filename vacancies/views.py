from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.http import HttpResponse
from . import models

class MainView(TemplateView):

    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies_by_category'] = models.Specialty.objects.all()
        return context

class AllVacancies(TemplateView):
    template_name = 'vacancies/vacancies.html'


class VacanciesByCategory(TemplateView):
    template_name = 'vacancies/vacancies.html'


class CompanyCard(TemplateView):
    template_name = 'vacancies/company.html'


class Vacancy(TemplateView):
    template_name = 'vacancies/vacancy.html'
