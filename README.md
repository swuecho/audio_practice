# Dev


## init data

0. init table

```
python manage.py migrate
```

1. create admin user

```bash
cd api
python manage.py createsuperuser
```

2. add permission data

```sh
# Load data
python manage.py loaddata data/permission.json 
python manage.py loaddata data/role.json 
python manage.py loaddata data/user_roles_role.json
python manage.py loaddata data/role_permissions.json
```


## web

```sh
cd web
npm run dev
```

## backend

```
# add env var
# export DEBUG=1
# export DATABASE_URL=postgresql://xxxx
# export SILICIONFLOW_API_KEY=sk-xxx
cd api
make dev
```


## FAQ

1. change pass

cd api
python manage.py runscript reset_password