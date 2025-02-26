import os
from datetime import timedelta

from django.http import HttpResponseForbidden, HttpResponseNotFound, FileResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from eske70ru import settings
from .models import Program, SoftDownload


def view_programs(request):
    programs = Program.objects.filter(is_active=True)
    context = {
        'title': 'Программы',
        'programs': programs if programs else [],
    }
    return render(request, 'programs/view_programs.html', context=context)


def program_detail(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    context = {
        'title': program.name,
        'program': program,
    }
    return render(request, 'programs/program_detail.html', context=context)


def download_program(request, program_id):
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
