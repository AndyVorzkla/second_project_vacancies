from django.contrib import admin
from . import models

admin.site.register(models.Specialty)
admin.site.register(models.Company)
admin.site.register(models.Vacancy)