from django.urls import path

from cloud.views import FileListView, upload_file, FileDetailView, create_file_link

urlpatterns = [
    path('files/', FileListView.as_view(), name='cloud'),
    path('files/get/<slug>', FileDetailView.as_view(), name='get_file'),
    path('files/<int:pk>', FileDetailView.as_view(), name='file_detail'),
    path('files/<int:pk>/create_link', create_file_link, name='create_file_link'),
    path('upload_file/', upload_file, name='upload_file'),
]
