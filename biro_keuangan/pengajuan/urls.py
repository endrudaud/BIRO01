from django.urls import path,include
from . import views
from .views import update_approval_status, create_user, user_list, toggle_admin_status, update_disposisi_pimpinan, upload_kwitansi

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_pengajuan, name='create_pengajuan'),
    path('tracking/', views.tracking_data, name='tracking_data'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_list/', user_list, name='user_list'),
    path('toggle_admin_status/<int:user_id>/', toggle_admin_status, name='toggle_admin_status'),
    path('update-approval/<int:pk>/', views.update_approval_status, name='update_approval_status'),
    path('create_user/', views.create_user, name='create_user'),
    path('upload-kwitansi/<int:pk>/', views.upload_kwitansi, name='upload_kwitansi'),
    path('update-disposisi/<int:pk>/', update_disposisi_pimpinan, name='update_disposisi_pimpinan'),
    path('upload-kwitansi/<int:pk>/', upload_kwitansi, name='upload_kwitansi'),

]
