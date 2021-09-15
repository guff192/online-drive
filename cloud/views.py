import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from cloud.models import File


class FileListView(LoginRequiredMixin, ListView):
    model = File

    def get_queryset(self):
        queryset = File.objects.filter(owner=self.request.user)
        return queryset


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            return HttpResponseRedirect(reverse_lazy('cloud'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


file_types = {
    'image': 'i',
    'audio': 'm',
    'video': 'v',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'd',
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

    name, content_type = uploaded_file.name, uploaded_file.content_type
    file_type = get_file_type(content_type)
    if not file_type:
        response.status_code = 400
        return response

    File.objects.create(
        file=uploaded_file,
        owner=current_user,
        name=name,
        file_type=file_type,
    )

    response.status_code = 200
    return response
