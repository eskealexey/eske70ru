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
    context = {
        'title': 'Программы',
        # 'programs': 'Нет программ',
    }
    return render(request, 'programs/view_programs.html', context=context)


def program_detail(request, program_id):
    """Просмотр программы"""
    program = Program.objects.get(id=program_id)
    context = {
        'title': program.name,
        'program': program,
    }
    return render(request, 'programs/program_detail.html', context=context)