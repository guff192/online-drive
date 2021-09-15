from django.urls import path

from cloud.views import FileListView

urlpatterns = [
    path('files/', FileListView.as_view(), name='cloud'),
]
