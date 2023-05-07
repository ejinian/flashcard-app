from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='flash-card-home'),
    path('hard_to_remember', views.hard_to_remember, name='hard-to-remember'),
    path('card_admin', views.card_admin, name='card-admin'),
    path('card_admin_create', views.card_admin_create, name='card-admin-create'),
    path('card_admin_delete', views.card_admin_delete, name='card-admin-delete'),
    path('card_admin_update/<int:pk>/', views.card_admin_update, name='card-admin-update'),
    path('admin_tool', views.admin_tool, name='admin-tool'),
]