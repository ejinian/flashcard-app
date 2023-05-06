from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='flash-card-home'),
    path('hard_to_remember', views.hard_to_remember, name='hard-to-remember'),
    path('card_admin', views.card_admin, name='card-admin'),
    path('admin_tool', views.admin_tool, name='admin-tool'),
]