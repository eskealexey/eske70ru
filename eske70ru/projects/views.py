from django.contrib.auth.decorators import login_required
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

#
# def project_detail(request, slug):
#     """
#     Детали проекта
#     """
#     if request.method == 'GET':
#         project = Project.objects.get(slug=slug)
#         form = CommentForm()
#         context = {
#             'project': project,
#             'title': project.title,
#             'form': form
#         }
#
#     return render(request, 'projects/project_detail.html', context=context)
#
#
# @login_required
# def add_comment(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.project = project
#             comment.author = request.user
#             comment.save()
#             return redirect('project_detail', slug=project.slug)
#     return redirect('project_detail', slug=project.slug)
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


@login_required
def add_comment(request, project_id):
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