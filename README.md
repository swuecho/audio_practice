# speaking practice

## Screenshot


<img width="1188" alt="001" src="https://github.com/user-attachments/assets/9b91881f-d617-4c91-9382-2e8c8d8f1ae8">

<img width="1098" alt="002" src="https://github.com/user-attachments/assets/6a41abfc-32ab-408a-94aa-8dfa233f4e3c">

# Dev


## init data

0. init table

```
#  export DATABASE_URL=postgresql://xxxx
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
python manage.py loaddata data/role_permission.json
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

## Credit

1. https://english-practice-app-nine.vercel.app/
2. https://github.com/ZuodaoTech/everyone-can-use-english

