# Generated by Django 4.2.13 on 2024-06-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengajuan', '0004_merge_0002_profile_0003_auto_20240602_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='kwitansi',
            name='upload_file',
            field=models.FileField(blank=True, null=True, upload_to='kwitansi/'),
        ),
    ]
