from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

def create_groups(apps, schema_editor):
    # Creating Admin Group
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        # Assign permissions to admin group
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)
    
    # Creating User Group
    user_group, created = Group.objects.get_or_create(name='User')
    if created:
        # Assign basic permissions to user group
        content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(content_type=content_type)
        user_group.permissions.set(user_permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('pengajuan', '0001_initial'),  # Adjust the dependency to match your initial migration
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
