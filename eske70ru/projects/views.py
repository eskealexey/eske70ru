from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.core.paginator import Paginator

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
    Подробная информация о проекте с пагинацией комментариев
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    comments_per_page = 15  # Количество комментариев на странице

    def get_object(self, queryset=None):
        project = super().get_object(queryset)

        session_key = f'project_viewed_{project.id}'
        if not self.request.session.get(session_key, False):
            Project.objects.filter(pk=project.pk).update(views=F('views') + 1)
            project.refresh_from_db()
            self.request.session[session_key] = True

        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Получаем активные комментарии
        comments = project.active_comments.all()

        # Создаем пагинатор
        paginator = Paginator(comments, self.comments_per_page)

        # Получаем номер страницы из GET-параметра
        page_number = self.request.GET.get('page')

        # Получаем страницу с комментариями
        page_obj = paginator.get_page(page_number)

        # Добавляем в контекст
        context['comment_form'] = CommentForm()
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['title'] = project.title

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
