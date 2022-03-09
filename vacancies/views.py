from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.http import HttpResponse, Http404
from . import models
from .models import Vacancy


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies_by_category'] = models.Specialty.objects.all()
        context['companies'] = models.Company.objects.all()
        return context


class AllVacancies(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Все вакансии'
        return context


class VacanciesByCategory(ListView):
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    # def get(self, request, *args, **kwargs):
    #     if kwargs['category_name'] not in [specialty.code for specialty in models.Specialty.objects.all()]:
    #         raise Http404
    #     else:
    #         return render(request, self.template_name, self.context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = models.Specialty.objects.get(code=self.specialty_code).title

        return context

    def get_queryset(self):
        self.specialty_code = self.kwargs['category_name']

        try:
            queryset = models.Vacancy.objects.filter(
                specialty=models.Specialty.objects.get(code=self.specialty_code)
            )
        except models.Specialty.DoesNotExist:
            raise Http404

        return queryset


class CompanyCard(ListView):
    template_name = 'vacancies/company.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['company'] = models.Company.objects.get(id=self.company_id)
        return context

    def get_queryset(self):
        self.company_id = self.kwargs['pk']

        try:
            queryset = models.Vacancy.objects.filter(company=models.Company.objects.get(id=self.company_id))
        except models.Company.DoesNotExist:
            raise Http404

        return queryset


class VacancyView(TemplateView):
    template_name = 'vacancies/vacancy.html'
    model = Vacancy
