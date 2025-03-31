from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from .forms import CommentForm
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


class ProjectDetailView(DetailView):
    """
    Подробная информация о проекте
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        # Получаем объект проекта
        project = super().get_object(queryset)

        # Логика подсчета просмотров
        session_key = f'project_viewed_{project.id}'
        if not self.request.session.get(session_key, False):
            # Атомарное обновление счетчика просмотров
            Project.objects.filter(pk=project.pk).update(views=F('views') + 1)
            # Обновляем объект проекта
            project.refresh_from_db()
            self.request.session[session_key] = True

        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


@login_required
def add_comment(request, project_id):
    """
    Добавление комментария
    """
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())

    return redirect('project_detail', slug=project.slug)