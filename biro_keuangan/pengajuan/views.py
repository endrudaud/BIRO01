# pengajuan/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SuratPengajuan
from .forms import SuratPengajuanForm

@login_required
def home(request):
    pengajuan_list = SuratPengajuan.objects.filter(user=request.user)
    return render(request, 'pengajuan/home.html', {'pengajuan_list': pengajuan_list})

@login_required
def create_pengajuan(request):
    if request.method == 'POST':
        form = SuratPengajuanForm(request.POST, request.FILES)
        if form.is_valid():
            surat = form.save(commit=False)
            surat.user = request.user
            surat.save()
            return redirect('home')
    else:
        form = SuratPengajuanForm()
    return render(request, 'pengajuan/create_pengajuan.html', {'form': form})

