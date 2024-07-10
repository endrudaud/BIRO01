# pengajuan/forms.py
from django import forms
from django.contrib.auth.models import User
from pengajuan.models import Profile
from .models import ApprovalKepalaBiro, DisposisiPimpinan, Kwitansi, SuratPengajuan

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_admin']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_admin = self.cleaned_data['is_admin']
            profile.save()
        return user

class SuratPengajuanForm(forms.ModelForm):
    class Meta:
        model = SuratPengajuan
        fields = ['judul', 'deskripsi', 'jumlah', 'upload_surat_pengajuan']
    class Meta:
        model = SuratPengajuan
        fields = ['judul', 'deskripsi', 'jumlah', 'upload_surat_pengajuan']

class ApprovalStatusForm(forms.ModelForm):
    class Meta:
        model = ApprovalKepalaBiro
        fields = ['approval_status', 'catatan']

class DisposisiPimpinanForm(forms.ModelForm):
    class Meta:
        model = DisposisiPimpinan
        fields = ['disposisi_status', 'catatan']

class ApprovalStatusForm(forms.ModelForm):
    class Meta:
        model = ApprovalKepalaBiro
        fields = ['approval_status', 'catatan']

class KwitansiForm(forms.ModelForm):
    class Meta:
        model = Kwitansi
        fields = ['upload_file']