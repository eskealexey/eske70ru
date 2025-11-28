from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from django.core.paginator import Paginator

from .forms import CommentForm
from .models import Project, ProjectFile


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


# class ProjectDetailView(DetailView):
#     """
#     Подробная информация о проекте с пагинацией комментариев
#     """
#     model = Project
#     template_name = 'projects/project_detail.html'
#     context_object_name = 'project'
#     comments_per_page = 15  # Количество комментариев на странице
#
#     def get_object(self, queryset=None):
#         project = super().get_object(queryset)
#
#         session_key = f'project_viewed_{project.id}'
#         if not self.request.session.get(session_key, False):
#             Project.objects.filter(pk=project.pk).update(views=F('views') + 1)
#             project.refresh_from_db()
#             self.request.session[session_key] = True
#
#         return project
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         project = self.object
#
#         # Получаем активные комментарии
#         comments = project.active_comments.all()
#
#         # Создаем пагинатор
#         paginator = Paginator(comments, self.comments_per_page)
#
#         # Получаем номер страницы из GET-параметра
#         page_number = self.request.GET.get('page')
#
#         # Получаем страницу с комментариями
#         page_obj = paginator.get_page(page_number)
#
#         # Добавляем в контекст
#         context['comment_form'] = CommentForm()
#         context['page_obj'] = page_obj
#         context['paginator'] = paginator
#         context['title'] = project.title
#
#         return context

#
# class ProjectDetailView(DetailView):
#     """
#     Подробная информация о проекте с пагинацией комментариев и файлами
#     """
#     model = Project
#     template_name = 'projects/project_detail.html'
#     context_object_name = 'project'
#     comments_per_page = 15  # Количество комментариев на странице
#
#     def get_object(self, queryset=None):
#         project = super().get_object(queryset)
#
#         session_key = f'project_viewed_{project.id}'
#         if not self.request.session.get(session_key, False):
#             Project.objects.filter(pk=project.pk).update(views=F('views') + 1)
#             project.refresh_from_db()
#             self.request.session[session_key] = True
#
#         return project
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         project = self.object
#
#         # Получаем активные комментарии
#         comments = project.active_comments.all()
#
#         # Получаем файлы проекта
#         project_files = project.active_files.all()
#
#         # Группируем файлы по типам для удобного отображения
#         files_by_type = {}
#         for file_type, file_type_display in ProjectFile.FILE_TYPES:
#             files_of_type = project_files.filter(file_type=file_type)
#             if files_of_type.exists():
#                 files_by_type[file_type_display] = files_of_type
#
#         # Создаем пагинатор для комментариев
#         paginator = Paginator(comments, self.comments_per_page)
#
#         # Получаем номер страницы из GET-параметра
#         page_number = self.request.GET.get('page')
#
#         # Получаем страницу с комментариями
#         page_obj = paginator.get_page(page_number)
#
#         # Добавляем в контекст
#         context['comment_form'] = CommentForm()
#         context['page_obj'] = page_obj
#         context['paginator'] = paginator
#         context['title'] = project.title
#         context['project_files'] = project_files
#         context['files_by_type'] = files_by_type
#         context['files_count'] = project.files_count
#         context['total_files_size'] = project.total_files_size
#
#         return context


class ProjectDetailView(DetailView):
    """
    Подробная информация о проекте с пагинацией комментариев и файлами
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    comments_per_page = 15

    def get_object(self, queryset=None):
        # Оптимизируем запрос, сразу подгружая связанные данные
        queryset = self.get_queryset().prefetch_related(
            'comments',
            'files'
        )
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
        comments = project.active_comments.select_related('author')

        # Получаем файлы проекта с оптимизацией
        project_files = project.active_files.all()

        # Детальная группировка файлов
        files_by_type = {}
        file_types_present = set()

        for file_obj in project_files:
            file_type = file_obj.file_type
            file_type_display = file_obj.get_file_type_display()
            print(file_type_display)

            if file_type not in files_by_type:
                files_by_type[file_type] = {
                    'display_name': file_type_display,
                    'files': [],
                    'count': 0,
                    'total_size': 0
                }
                file_types_present.add(file_type)

            files_by_type[file_type]['files'].append(file_obj)
            files_by_type[file_type]['count'] += 1
            files_by_type[file_type]['total_size'] += file_obj.size

        # Создаем пагинатор для комментариев
        paginator = Paginator(comments, self.comments_per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)



        # Добавляем в контекст
        context.update({
            'comment_form': CommentForm(),
            'page_obj': page_obj,
            'paginator': paginator,
            'title': project.title,
            'project_files': project_files,
            'files_by_type': files_by_type,
            'files_count': project.files_count,
            'total_files_size': get_file_size_display(project.total_files_size),
            'file_types_present': file_types_present,
        })

        return context

def get_file_size_display(size):
    """Возвращает размер файла в удобном формате"""
    if size < 1024:
        return f"{size} Б"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} КБ"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} МБ"
    else:
        return f"{size / (1024 * 1024 * 1024):.1f} ГБ"


class ProjectFileDownloadView(View):
    def get(self, request, file_id):
        project_file = get_object_or_404(ProjectFile, id=file_id, is_active=True)

        # Увеличиваем счетчик скачиваний
        project_file.increment_download_count()

        response = FileResponse(project_file.file.open(), as_attachment=True)
        response[
            'Content-Disposition'] = f'attachment; filename="{project_file.name}{project_file.get_file_extension()}"'
        return response



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
