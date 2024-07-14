from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_pengajuan, name='create_pengajuan'),
    path('tracking/', views.tracking_data, name='tracking_data'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_list/', views.user_list, name='user_list'),
    path('toggle_admin_status/<int:user_id>/', views.toggle_admin_status, name='toggle_admin_status'),
    path('update-approval/<int:pk>/', views.update_approval_status, name='update_approval_status'),
    path('create_user/', views.create_user, name='create_user'),
    path('upload_kwitansi/<int:pk>/', views.upload_kwitansi, name='upload_kwitansi'),
    path('update-disposisi/<int:pk>/', views.update_disposisi_pimpinan, name='update_disposisi_pimpinan'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('view_kwitansi/<int:pk>/', views.view_kwitansi, name='view_kwitansi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)