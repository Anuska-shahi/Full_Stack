from django.urls import path
from .views import CustomUserListView, CustomUserDetailView, CustomUserRestoreView, CustomUserHardDeleteView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    # path('users/', CustomUserListView.as_view(), name='user-list'),
    # path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    # path('users/<int:pk>/restore/', CustomUserRestoreView.as_view(), name='user_restore'),
    # path('users/<int:pk>/hard-delete/', CustomUserHardDeleteView.as_view(), name='user_hard_delete'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', CustomUserListView.user_list, name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.user_detail, name='user-detail'),
    path('users/<int:pk>/restore/', CustomUserRestoreView.user_restore, name='user_restore'),
    path('users/<int:pk>/hard-delete/', CustomUserHardDeleteView.user_hard_delete, name='user_hard_delete'),
    path('login/', LoginView.login_authentication, name='login'),
    path('logout/', LoginView.logout, name='login'),
]



