from django.shortcuts import render

from .models import Program


# Create your views here.
def view_programs(request):
    """Просмотр списка программ"""
    programs = Program.objects.all()
    if programs:
        context = {
            'title': 'Программы',
            'programs': programs,
        }
        return render(request, 'programs/view_programs.html', context=context)
    else:
        context = {
            'title': 'Программы',
            'programs': 'Нет программ',
        }
        return render(request, 'programs/view_programs.html', context=context)
