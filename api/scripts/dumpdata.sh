# Dump data
python manage.py dumpdata admin_backend.permission > data/permission.json
python manage.py dumpdata admin_backend.role > data/role.json
python manage.py dumpdata admin_backend.userrolesrole > data/user_roles_role.json
python manage.py dumpdata admin_backend.rolepermissionspermission > data/role_permissions.json