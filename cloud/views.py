import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from cloud.forms import CreateFileLinkForm
from cloud.models import File


def disk_space_used(user):
    user_files = File.objects.filter(owner=user)
    space_used = 0
    for f in user_files:
        space_used += f.file.size
    return space_used


class FileListView(LoginRequiredMixin, ListView):
    model = File

    def get_queryset(self):
        queryset = File.objects.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FileListView, self).get_context_data(object_list=object_list, **kwargs)
        context['disk_space_used'] = round(disk_space_used(self.request.user) / 10**6, 1)
        return context


class FileDetailView(DetailView):
    model = File

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if kwargs.get('slug'):
            slug = kwargs['slug']
            print(slug)
            if not slug.split('-')[0].isdigit() and not request.user.is_authenticated:
                return HttpResponseRedirect(reverse_lazy('login'))

        elif self.object.owner != self.request.user:
            return HttpResponseRedirect(reverse_lazy('cloud'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


file_types = {
    'image': 'i',
    'audio': 'm',
    'video': 'v',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'd',
    'application/pdf': 'd',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'p',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 't',
}


def get_file_type(content_type):
    global file_types
    if file_types.get(content_type, False):
        file_type = file_types[content_type]
    elif file_types.get(content_type.split('/')[0], False):
        file_type = file_types[content_type.split('/')[0]]
    else:
        file_type = None
    return file_type


def upload_file(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse_lazy('cloud'))

    response = HttpResponse()

    uploaded_file = request.FILES['file']
    if (disk_space_used(current_user) + uploaded_file.size) / 10**6 >= 15:
        response.status_code = 403
        response.content = 'Лимит допустимого пространства превышен'
        return response

    name, content_type = uploaded_file.name, uploaded_file.content_type
    print(content_type)
    file_type = get_file_type(content_type)
    if not file_type:
        response.status_code = 400
        response.content = 'Недопустимый формат файла'
        return response

    File.objects.create(
        file=uploaded_file,
        owner=current_user,
        name=name,
        file_type=file_type,
    )

    response.status_code = 200
    response.content = 'Файл успешно загружен'
    return response


def create_file_link(request, pk):
    current_user = request.user
    file = File.objects.get(pk=pk)
    response = HttpResponse()
    if file.owner != current_user:
        response.status_code = 403
        return response

    if request.method == 'POST':
        form = CreateFileLinkForm(request.POST)
        if form.is_valid():
            file.public = bool(form.data.get('public'))
            print(file.public)
            if file.public:
                slug_chr = chr(random.randint(48, 57))
            else:
                slug_chr = chr(random.randint(97, 122))
            file.slug = slugify(f"{slug_chr} {file.pk} {file.name.split('.')[:-1]}", True)
            file.save()
            return HttpResponseRedirect(reverse('file_detail', args=[str(pk)]))

    form = CreateFileLinkForm(instance=file)
    context = {'form': form}
    return render(request, 'cloud/create_file_link_form.html', context)
