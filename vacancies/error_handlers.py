from django.http import HttpResponseServerError, HttpResponseNotFound


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 ошибка!')


def custom_handler500(request):
    return HttpResponseServerError('500 ошибка!')
