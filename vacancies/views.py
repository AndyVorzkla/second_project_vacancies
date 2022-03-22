from pyexpat.errors import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView, View
from django.http import Http404, HttpResponseRedirect
from . import models, forms


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['vacancies_by_category'] = models.Specialty.objects.all()
        context['companies'] = models.Company.objects.all()
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
    template_name = 'vacancies/week4/company-create.html'


class MyCompanyCreate(TemplateView):
    template_name = 'vacancies/week4/company-edit_blank.html'

    def get(self, request, *args, **kwargs):
        try:
            company = request.user.company
            return redirect('my_company') # если компани уже есть, то отправляет обратно к редактированию

        except ObjectDoesNotExist:
            form = forms.Company()
            return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.Company(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            models.Company.objects.create(
                name=data['name'],
                logo=data['logo'],
                city=data['city'],
                description=data['description'],
                employee_count=data['employee_count'],
                owner=request.user
            )

            return redirect('my_company')
        else:
            return render(request, template_name=self.template_name, context={'form': form})


class MyCompanyFill(TemplateView):
    # если есть то MyCompanyFill если нет то MyCompanyStart>MyCompanyBlank
    template_name = 'vacancies/week4/company-edit.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            company = user.company
            form = forms.Company(
                {
                    'name': user.company.name,
                    'city': user.company.city,
                    'description': user.company.description,
                    'employee_count': user.company.employee_count,
                    'logo': user.company.logo,
                    'owner': user
                }
            )
            return render(request, template_name=self.template_name, context={'form': form, 'company': company})

        except ObjectDoesNotExist:
            return redirect('lets_start')

    def post(self, request, *args, **kwargs):
        company = request.user.company
        form = forms.Company(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()

            return redirect('my_company')
        else:
            render(request, template_name=self.template_name, context={'form': form, 'company': company})


class MyCompanyVacancies(View):
    template_name = 'vacancies/week4/vacancy-list.html'
    context_object_name = 'vacancies'

    def get(self, request, *args, **kwargs):
        company_id = request.user.company.id
        vacancies = models.Vacancy.objects.filter(company__id=company_id).values(
            'title',
            'salary_max',
            'pk',
        ).annotate(applications_count=Count('applications'))
        if vacancies.exists():  # or if vacancies:
            context = {
                'vacancies': vacancies,
            }
            return render(request, template_name=self.template_name, context=context)
        else:
            return redirect('lets_start_vacancy') # редирект на создание компании


class MyCompanyVacanciesStart(TemplateView):
    template_name = 'vacancies/week4/vacancy-letsstart.html'


class MyCompanyVacancyCreate(TemplateView):
    template_name = 'vacancies/week4/vacancy-edit_blank.html'

    def get(self, request, *args, **kwargs):
        form = forms.VacancyForm()
        return render(request, template_name=self.template_name, context={'form': form, 'title': ''})

    def post(self, request, *args, **kwargs):
        form = forms.VacancyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            models.Vacancy.objects.create(
                title=data['title'],
                specialty=data['specialty'],
                skills=data['skills'],
                text=data['text'],
                company=request.user.company,
                salary_min=data['salary_min'],
                salary_max=data['salary_max'],
            )
            return redirect('company_vacancies')
        else:
            return render(request, template_name=self.template_name, context={'form': form, 'title': ''})


class MyCompanyVacancyFill(UpdateView):
    template_name = 'vacancies/week4/vacancy-edit.html'
    model = models.Vacancy
    form_class = forms.VacancyForm
    success_url = '/mycompany/vacancies/'


class ApplicationsView(ListView):
    template_name = 'vacancies/week4/applications.html'
    context_object_name = 'applications'
    vacancy = None

    def get_queryset(self):
        self.vacancy = get_object_or_404(models.Vacancy, pk=self.kwargs['pk'])
        if self.vacancy.company.owner != self.request.user: # как итерироваться если у юзера будет много компаний
            raise Http404()
        return self.vacancy.applications.all()





