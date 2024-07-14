from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SuratPengajuan, ApprovalKepalaBiro, Kwitansi, DisposisiPimpinan
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from .forms import UserCreationForm, ApprovalStatusForm, SuratPengajuanForm, DisposisiPimpinanForm, KwitansiForm
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import logging

logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'pengajuan/create_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.profile.is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'pengajuan/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.profile.is_admin)
def toggle_admin_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    profile.is_admin = not profile.is_admin
    profile.save()
    return redirect('user_list')

def admin_check(user):
    return user.is_authenticated and user.profile.is_admin

def is_admin_setama(user):
    return user.groups.filter(name='admin_setama').exists()

def is_admin_01(user):
    return user.groups.filter(name='admin_01').exists()

@login_required
def update_approval_status(request, pk):
    approval = get_object_or_404(ApprovalKepalaBiro, pk=pk)
    if request.method == 'POST':
        form = ApprovalStatusForm(request.POST, instance=approval)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ApprovalStatusForm(instance=approval)
    return render(request, 'pengajuan/update_approval_status.html', {'form': form})

@login_required
def update_disposisi_pimpinan(request, pk):
    pengajuan = get_object_or_404(SuratPengajuan, pk=pk)
    disposisi = pengajuan.disposisipimpinan_set.first()
    if request.method == 'POST':
        form = DisposisiPimpinanForm(request.POST, instance=disposisi)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DisposisiPimpinanForm(instance=disposisi)
    return render(request, 'pengajuan/update_disposisi_pimpinan.html', {'form': form})

@login_required
def create_pengajuan(request):
    if request.method == 'POST':
        form = SuratPengajuanForm(request.POST, request.FILES)
        if form.is_valid():
            surat = form.save(commit=False)
            surat.user = request.user
            surat.save()
            
            if not ApprovalKepalaBiro.objects.filter(surat_pengajuan=surat).exists():
                ApprovalKepalaBiro.objects.create(surat_pengajuan=surat)
            
            DisposisiPimpinan.objects.create(surat_pengajuan=surat)

            return redirect('home')
    else:
        form = SuratPengajuanForm()
    return render(request, 'pengajuan/create_pengajuan.html', {'form': form})

@login_required
def tracking_data(request):
    return render(request, 'pengajuan/tracking_data.html')

@receiver(post_save, sender=SuratPengajuan)
def create_approval_kepala_biro(sender, instance, created, **kwargs):
    if created:
        ApprovalKepalaBiro.objects.create(surat_pengajuan=instance)

@login_required
def upload_kwitansi(request, pk):
    pengajuan = get_object_or_404(SuratPengajuan, pk=pk)
    if request.method == 'POST':
        form = KwitansiForm(request.POST, request.FILES)
        if form.is_valid():
            kwitansi = form.save(commit=False)
            kwitansi.surat_pengajuan = pengajuan
            kwitansi.save()
            pengajuan.kwitansi_filled = True
            pengajuan.status = 'selesai'
            pengajuan.save()
            return redirect('home')
    else:
        form = KwitansiForm()
    return render(request, 'pengajuan/upload_kwitansi.html', {'form': form})

@login_required
def view_kwitansi(request, pk):
    kwitansi = get_object_or_404(Kwitansi, surat_pengajuan_id=pk)
    file_path = kwitansi.upload_file.path
    if not os.path.exists(file_path):
        raise Http404("File does not exist")

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response


@login_required
def home(request):
    if request.user.profile.is_admin:
        pengajuan_list = SuratPengajuan.objects.all()
    else:
        pengajuan_list = SuratPengajuan.objects.filter(user=request.user)
    
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'id')
    
    if search_query:
        pengajuan_list = pengajuan_list.filter(
            Q(judul__icontains=search_query) |
            Q(deskripsi__icontains=search_query) |
            Q(jumlah__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    if sort_by in ['id', 'judul', 'jumlah']:
        pengajuan_list = pengajuan_list.order_by(sort_by)
    
    paginator = Paginator(pengajuan_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pengajuan/home.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'is_admin': request.user.profile.is_admin,
    })
