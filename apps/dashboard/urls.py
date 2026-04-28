from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/agencies/', views.admin_agencies, name='agencies'),
    path('admin/agencies/<uuid:agency_id>/action/', views.approve_agency, name='approve_agency'),
    path('admin/users/', views.admin_users, name='users'),
]
