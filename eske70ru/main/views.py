# Create your views here.
from django.shortcuts import render


def index(request):

    context = {
        'title': 'Главная страница',
    }
    return render(request, 'main/main.html', context=context)

