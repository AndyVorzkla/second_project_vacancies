from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView, View
from django.http import Http404, HttpResponseRedirect
from . import models, forms


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies_by_category'] = models.Specialty.objects.all()
        context['companies'] = models.Company.objects.all()
        print(self.request.user)
        return context


class AllVacancies(ListView):
    model = models.Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Все вакансии'
        return context


class VacanciesByCategory(ListView):
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'
    specialty = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.speciality.title

        return context

    def get_queryset(self):
        self.speciality = get_object_or_404(models.Specialty, code=self.kwargs['category_name'])

        return self.speciality.vacancies.all()


class CompanyCard(ListView):
    template_name = 'vacancies/company.html'
    context_object_name = 'vacancies'
    company_id = None

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.company_id = self.kwargs['pk']

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


class VacancyView(DetailView):
    # по дефолту, DetailView сам фильтрует запись по <int:pk>, если он так указан в urls
    template_name = 'vacancies/vacancy.html'
    model = models.Vacancy
    extra_context = {'form': forms.Application}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = forms.Application(request.POST)
        id = self.kwargs['pk']
        if form.is_valid():
            data = form.cleaned_data
            application = models.Application(**data, user=request.user, vacancy=models.Vacancy.objects.get(id=id))
            application.save()
            return redirect('send_vacancy', pk=id)
        else:
            object = models.Vacancy.objects.get(id=id)
            return render(request, self.template_name, context={'form': form, 'object': object})




def test(request, *args, **kwargs):
    template_name = 'vacancies/test.html'
    if request.method.lower() == 'get':
        return render(request, template_name, context={'form': forms.Application})
    if request.method.lower() == 'post':
        form = forms.PostcardForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print(form.data.get)
            return redirect('test')
        return render(request, template_name, context={'form': form})


class VacancySend(DetailView):
    template_name = 'vacancies/week4/sent.html'
    model = models.Vacancy

class MyCompanyStart(TemplateView):
    template_name = ''

class MyCompanyBlank(TemplateView):
    template_name = 'vacancies/week4/company-create.html'

class MyCompanyFill(TemplateView):
    # если есть то MyCompanyFill если нет то MyCompanyBlank
    template_name = 'vacancies/week4/company-edit.html'

class MyCompanyVacancies(TemplateView):
    template_name = 'vacancies/week4/vacancy-list.html'

class MyCompanyVacancyBlank(TemplateView):
    template_name = ''

class MyCompanyVacancyFill(TemplateView):
    template_name = 'vacancies/week4/vacancy-edit.html'




