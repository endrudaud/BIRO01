from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_pengajuan, name='create_pengajuan'),
    path('tracking/', views.tracking_data, name='tracking_data'),
    path('accounts/', include('django.contrib.auth.urls')),
]
