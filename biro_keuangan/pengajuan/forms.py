# pengajuan/forms.py
from django import forms
from .models import SuratPengajuan

class SuratPengajuanForm(forms.ModelForm):
    class Meta:
        model = SuratPengajuan
        fields = '__all__'
        exclude = ['user', 'approval_kepala_biro', 'kwitansi_filled', 'status', 'tanggal_pengajuan', 'created_at', 'updated_at']
