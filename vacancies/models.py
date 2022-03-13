from enum import Enum

from django.db import models
from django.urls import reverse
# from mptt.models import MPTTModel, TreeForeignKey #  if we have Tree on ForeignKey. (Вложенность моделей на self)

class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=60)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return (f'Specialty {self.code}')


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()

    def __str__(self):
        return f'Company {self.name}'


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company'
    )
    # related_name - имя отображения в админ. панели
    skills = models.CharField(max_length=60)
    text = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()

    def skills_as_list(self):
        return [skill.strip() for skill in self.skills.split(',')]

    def __str__(self):
        return f'Vacancy {self.title}'

    def get_absolute_url(self):
        """
        Get absolute url, add in admin panel 'view on site' button
        Other variant to add url in href
        :return:
        """
        return reverse('vacancy_pk', kwargs={'pk': self.id})
        # return reverse('test_with_variables', kwargs={'name':self.specialty.code, 'pk': self.id})

    class Meta:
        verbose_name = 'Вакансии'  # used to display custom name in admin panel. Automaticly add 's' to the end
        verbose_name_plural = 'Вакансии'  # Fixed that

    # class MPTTMeta:
    #     order_insertion_by = ['title']
    # def specialty_rus(self):
    #     return getattr(SpecialtyChoices, str(self.specialty).split()[-1]).value


class SpecialtyChoices(Enum):
    frontend = 'Фронтенд'
    backend = 'Бэкенд'
    gamedev = 'Геймдев'
    devops = 'Девопс'
    design = 'Дизайн'
    products = 'Продукты'
    management = 'Менеджмент'
    testing = 'Тестирование'


class Application(models.Model):
    written_username = models.CharField(max_length=120)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications'
    )
    image = models.ImageField
