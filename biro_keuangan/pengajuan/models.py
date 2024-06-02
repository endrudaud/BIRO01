from django.db import models
from django.contrib.auth.models import User

class SuratPengajuan(models.Model):
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disposisi_pimpinan = models.BooleanField(default=False)
    approval_kepala_biro = models.BooleanField(default=False)
    kwitansi_filled = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upload_surat_pengajuan = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.judul

class DisposisiPimpinan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    surat_pengajuan = models.ForeignKey(SuratPengajuan, on_delete=models.CASCADE)
    disposisi_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_disposisi = models.DateTimeField(auto_now_add=True)
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.surat_pengajuan} - {self.disposisi_status}'

class ApprovalKepalaBiro(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    surat_pengajuan = models.ForeignKey(SuratPengajuan, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_approval = models.DateTimeField(auto_now_add=True)
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.surat_pengajuan} - {self.approval_status}'

class Kwitansi(models.Model):
    surat_pengajuan = models.ForeignKey(SuratPengajuan, on_delete=models.CASCADE)
    tanggal_pengisian = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.surat_pengajuan} - {self.amount}'
