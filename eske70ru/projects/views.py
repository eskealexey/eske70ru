from django.shortcuts import render

from .models import Project

# Create your views here.
def view_projects(request):
    """
    Список проектов
    """
    projects = Project.objects.all()

    context = {
        'projects': projects,
        'title': 'Проекты',
    }
    return render(request, 'projects/projects_all.html', context=context)