from django.db import migrations

def setup_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model('accounts', 'User')

    def perms(app_label, *codenames):
        return list(
            Permission.objects.filter(
                content_type__app_label=app_label,
                codename__in=codenames
            )
        )

    # Grupos
    usuarios, _ = Group.objects.get_or_create(name='Usuarios')
    mentores, _ = Group.objects.get_or_create(name='Mentores')
    empresas, _ = Group.objects.get_or_create(name='Empresas')
    administradores, _ = Group.objects.get_or_create(name='Administradores')

    # Para rodar de novo sem duplicar/bugar
    usuarios.permissions.clear()
    mentores.permissions.clear()
    empresas.permissions.clear()
    administradores.permissions.clear()

    # ---- Usuarios (usuário comum) ----
    usuarios.permissions.add(*perms('accounts', 'view_user', 'change_user'))
    usuarios.permissions.add(*perms(
        'avatar',
        'view_avatarprofile', 'change_avatarprofile',
        'view_userinventory', 'change_userinventory',
        'view_avataritem'
    ))
    usuarios.permissions.add(*perms('missions', 'view_mission', 'view_subtask'))
    usuarios.permissions.add(*perms('dashboard', 'view_achievement', 'view_activityevent', 'view_userachievement'))

    # ---- Mentores ----
    mentores.permissions.add(*perms('accounts', 'view_user'))
    mentores.permissions.add(*perms(
        'missions',
        'add_mission', 'change_mission', 'view_mission',
        'add_subtask', 'change_subtask', 'view_subtask'
    ))
    mentores.permissions.add(*perms('dashboard', 'view_achievement', 'view_activityevent', 'view_userachievement'))
    mentores.permissions.add(*perms('avatar', 'view_avatarprofile', 'view_userinventory', 'view_avataritem'))

    # ---- Empresas ----
    empresas.permissions.add(*perms('accounts', 'view_user'))
    empresas.permissions.add(*perms('dashboard', 'view_achievement', 'view_activityevent', 'view_userachievement'))
    empresas.permissions.add(*perms('missions', 'view_mission', 'view_subtask'))
    empresas.permissions.add(*perms('avatar', 'view_avatarprofile', 'view_userinventory', 'view_avataritem'))

    # ---- Administradores (tudo do projeto) ----
    for app_label in ['accounts', 'avatar', 'dashboard', 'missions']:
        administradores.permissions.add(
            *Permission.objects.filter(content_type__app_label=app_label)
        )

    # Usuários antigos que não estão em nenhum grupo -> "Usuarios"
    for u in User.objects.all():
        if not u.is_superuser and not u.groups.exists():
            u.groups.add(usuarios)

def reverse_setup_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for name in ['Usuarios', 'Mentores', 'Empresas', 'Administradores']:
        Group.objects.filter(name=name).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_user_level_user_xp'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(setup_groups, reverse_setup_groups),
    ]
