from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SuratPengajuan
from .forms import SuratPengajuanForm

@login_required
def home(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'id')
    
    pengajuan_list = SuratPengajuan.objects.filter(user=request.user)
    
    if search_query:
        pengajuan_list = pengajuan_list.filter(
            Q(judul__icontains=search_query) |
            Q(deskripsi__icontains=search_query) |
            Q(jumlah__icontains=search_query) |
            Q(disposisi_pimpinan__icontains=search_query) |
            Q(approval_kepala_biro__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    
    if sort_by in ['id', 'judul', 'jumlah', 'disposisi_pimpinan']:
        pengajuan_list = pengajuan_list.order_by(sort_by)
    
    paginator = Paginator(pengajuan_list, 20)  # Show 20 pengajuan per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pengajuan/home.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required
def create_pengajuan(request):
    if request.method == 'POST':
        form = SuratPengajuanForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            surat = form.save(commit=False)
            surat.user = request.user
            surat.save()
            return redirect('home')
    else:
        form = SuratPengajuanForm()
    return render(request, 'pengajuan/create_pengajuan.html', {'form': form})

@login_required
def tracking_data(request):
    return render(request, 'pengajuan/tracking_data.html')
