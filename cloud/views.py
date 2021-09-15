from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from cloud.models import File


class FileListView(LoginRequiredMixin, ListView):
    model = File

    def get_queryset(self):
        queryset = File.objects.filter(owner=self.request.user)
        return queryset
