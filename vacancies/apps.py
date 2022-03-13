from django.apps import AppConfig


class VacanciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vacancies'
    # verbose_name = 'Вакансии' Если подключить в INST APPS вместо vacancies - vacancies.apps.VacanciesConfig,
    # то будет отображаться в админ панели имя varbose_name
