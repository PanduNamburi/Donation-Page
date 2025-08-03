from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    
    # Core data endpoints
    path('intern/', views.intern_data, name='intern_data'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    
    # Notifications endpoints
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Donations endpoint (public)
    path('donations/add/', views.add_donation, name='add_donation'),
    
    # Frontend pages
    path('', views.serve_static_file, {'filename': 'index.html'}, name='index'),
    path('login/', views.serve_static_file, {'filename': 'login.html'}, name='login'),
    path('dashboard/', views.serve_static_file, {'filename': 'dashboard.html'}, name='dashboard'),
    path('leaderboard-page/', views.serve_static_file, {'filename': 'leaderboard.html'}, name='leaderboard_page'),
    path('donate/', views.serve_static_file, {'filename': 'donate.html'}, name='donate'),
] 