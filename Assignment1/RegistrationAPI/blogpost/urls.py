from django.urls import path
from .views import BlogListView,BlogDetailView,BlogPostHardDeleteView,BlogRestoreView

urlpatterns=[
    path('blogs/',BlogListView.blog_list,name='blog-list'),
    path('blogs/<int:pk>/',BlogDetailView.blog_detail,name='blog-detail'),
    path('blogs/<int:pk>/restore/', BlogRestoreView.blog_restore, name='blog_restore'),
    path('blogs/<int:pk>/hard-delete/', BlogPostHardDeleteView.blog_hard_delete, name='blog_hard_delete'),
]