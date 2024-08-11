

# web

```sh
cd web
npm run build

# copy to backend server
cd ..
mkdir -p ./api/staticfiles
cp -r ./web/dist/* ./api/staticfiles/
```

# backend

```
python manage.py runserver 0.0.0.0:8000
```