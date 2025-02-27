import os
from datetime import timedelta

from django.http import HttpResponseForbidden, HttpResponseNotFound, FileResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from eske70ru import settings
from .models import Program, SoftDownload


def view_programs(request):
    """Вывод списка программ"""
    programs = Program.objects.filter(is_active=True)
    downloads_dict = {
        program.id: SoftDownload.objects.filter(program_id=program.id)
        for program in programs
    }
    dict_count = {}
    for program_id, downloads in downloads_dict.items():
        sch = 0
        for download in downloads:
            sch += download.count
        dict_count[program_id] = sch
        # print(f"Программа {program_id}: {sch} скачиваний")
    print(dict_count)

    context = {
        'title': 'Программы',
        'programs': programs if programs else [],
        'count_downloads': dict_count,
    }
    return render(request, 'programs/view_programs.html', context=context)
# def view_programs(request):
#     """Вывод списка программ"""
#     programs = Program.objects.filter(is_active=True).annotate(
#         total_downloads=Sum('softdownload__count')
#     )
#
#     context = {
#         'title': 'Программы',
#         'programs': programs,
#         'count_downloads': {program.id: program.total_downloads or 0 for program in programs},
#     }
#     return render(request, 'programs/view_programs.html', context=context)


def program_detail(request, program_id):
    """Вывод программы"""
    program = get_object_or_404(Program, id=program_id)
    counter = SoftDownload.objects.filter(program_id=program_id)
    count = 0
    for c in counter:
        count += c.count

    context = {
        'title': program.name,
        'program': program,
        'counter': count,
    }
    return render(request, 'programs/program_detail.html', context=context)


def download_program(request, program_id):
    """Скачивание программы"""
    ip_address = request.META.get('REMOTE_ADDR', '')
    program = get_object_or_404(Program, id=program_id)

    if not program.file:
        return HttpResponseNotFound("Файл не прикреплен")

    file_path = program.file.path
    allowed_dir = os.path.abspath(settings.MEDIA_ROOT)

    if not file_path.startswith(allowed_dir):
        return HttpResponseForbidden("Доступ запрещен")

    if not os.path.exists(file_path):
        return HttpResponseNotFound("Файл не найден")

    # Логика подсчета скачиваний
    soft_instance, created = SoftDownload.objects.get_or_create(
        program_id=program_id,
        ip_remote=ip_address,
        defaults={'count': 1, 'date': timezone.now()}
    )

    if not created:
        time_delta = timezone.now() - soft_instance.date
        if time_delta > timedelta(minutes=15):
            soft_instance.count += 1
            soft_instance.date = timezone.now()
            soft_instance.save()

    try:
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    except FileNotFoundError:
        return HttpResponseNotFound("Файл не найден")
