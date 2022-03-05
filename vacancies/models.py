from django.db import models


class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=60)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return(f'Specialty {self.code}')

class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


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
    skills = models.CharField(max_length=60)
    text = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()



