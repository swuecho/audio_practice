version=0.1.24
local_registry=192.168.0.100:5555
aliyun_registry_bestqa=registry.cn-shanghai.aliyuncs.com/bestqa
github_pkg_registry_surveyresearch=docker.pkg.github.com/swuecho/surveyresearch

static:
	rm -rf staticfiles
	mkdir staticfiles
	# cp -rf templates/components staticfiles/components
	python manage.py collectstatic --noinput
	cp -rf  ../web/dist/* staticfiles
dev:
	echo $DEBUG
	echo $DATABASE_URL
	python manage.py runserver 0.0.0.0:8001

serve:
	echo $DEBUG
	echo $DATABASE_URL
	gunicorn --bind 0.0.0.0:8001 --workers 2 admin_backend.wsgi:application


tag:
	git tag release-v$(version)
	git push origin tag release-v$(version)

build:
	docker build  -t $(local_registry)/admin_backend:$(version) -f Dockerfile .
push:
	docker push $(local_registry)/admin_backend:$(version)

push_aliyun:
	docker tag  $(local_registry)/admin_backend:$(version) $(aliyun_registry_bestqa)/admin_backend:$(version)
	docker push $(aliyun_registry_bestqa)/admin_backend:$(version)

init:
	python manage.py migrate
	# 对应 01_auth_init
	python manage.py runscript auth_init 
