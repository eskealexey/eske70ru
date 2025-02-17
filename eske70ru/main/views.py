from django.shortcuts import render


# Create your views here.
def index(request):

    context = {
        'title': 'Удобрения',
    }
    return render(request, 'main/main.html', context=context)