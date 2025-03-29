from django.shortcuts import render

from .models import Project

# Create your views here.
def view_projects(request):
    """
    Список проектов
    """
    projects = Project.objects.all().filter(status='published')

    context = {
        'projects': projects,
        'title': 'Проекты',
    }
    return render(request, 'projects/projects_all.html', context=context)


def project_detail(request, slug):
    """
    Детали проекта
    """
    if request.method == 'GET':
        project = Project.objects.get(slug=slug)
        context = {
            'project': project,
            'title': project.title,
        }

    return render(request, 'projects/project_detail.html', context=context)

