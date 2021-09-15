from django.urls import path

from cloud.views import FileListView, upload_file, FileDetailView

urlpatterns = [
    path('files/', FileListView.as_view(), name='cloud'),
    path('files/<int:pk>', FileDetailView.as_view(), name='file_detail'),
    path('upload_file/', upload_file, name='upload_file'),
]
