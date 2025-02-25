from django.shortcuts import render, redirect

from .models import Program


# Create your views here.
def view_programs(request):
    """Просмотр списка программ"""
    programs = Program.objects.filter(is_active=True)
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
        'download': program.file,
    }
    return render(request, 'programs/program_detail.html', context=context)


def download_program(request, program_id):
    """Подсчет количества программ"""
    print(program_id)
    count = 0
    if request.method == 'GET':
        ip = request.META['REMOTE_ADDR']
        session = request.session.session_key
        print(ip, session)

        count += 1
        print(count)
    # context = {
    #     'title': program.name,
    #     'program': program,
    #     'download': program.file,
    # }
    return redirect('program_detail', program_id)