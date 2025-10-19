from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
]
