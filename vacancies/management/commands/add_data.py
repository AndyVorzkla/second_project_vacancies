from django.core.management.base import BaseCommand
import data
from vacancies.models import Specialty, Company, Vacancy


class Command(BaseCommand):
    """
    optional --add_all to update the DataBase with content of data.py
    """

    def add_arguments(self, parser):
        parser.add_argument('--add_all', action='store_true', help='Add all data from data.py')

    def handle(self, *args, **options):
        if options['add_all']:
            for specialty in data.specialties:
                specialty_save_db = Specialty(
                    code=specialty['code'],
                    title=specialty['title'],
                )
                specialty_save_db.save()

            for company in data.companies:
                company_save_db = Company(
                    id=company['id'],
                    name=company['title'],
                    city=company['location'],
                    logo=company['logo'],
                    description=company['description'],
                    employee_count=company['employee_count'],
                )
                company_save_db.save()

            for vacancie in data.jobs:
                try:
                    specialty_fk = Specialty.objects.get(code=vacancie['specialty'])
                    company_fk = Company.objects.get(id=vacancie['id'])
                except Specialty.DoesNotExist:
                    print('Specialty name error')
                except Company.DoesNotExist:
                    print('Company name error')

                vacancie_save_db = Vacancy(
                    id=vacancie['id'],
                    title=vacancie['title'],
                    specialty=specialty_fk,
                    company=company_fk,
                    skills=vacancie['skills'],
                    text=vacancie['description'],
                    salary_min=int(vacancie['salary_from']),
                    salary_max=int(vacancie['salary_to']),
                    published_at=vacancie['posted']
                )
                vacancie_save_db.save()
