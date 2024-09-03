version=0.2.1
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
	gunicorn --bind 0.0.0.0:8001 --workers 2 practice_audio.wsgi:application


tag:
	git tag release-v$(version)
	git push origin tag release-v$(version)

build: static
	docker build  -t $(local_registry)/practice_audio:$(version) -f Dockerfile .
push:
	docker push $(local_registry)/practice_audio:$(version)

push_aliyun:
	docker tag  $(local_registry)/practice_audio:$(version) $(aliyun_registry_bestqa)/practice_audio:$(version)
	docker push $(aliyun_registry_bestqa)/practice_audio:$(version)

init:
	python manage.py migrate
	# 对应 01_auth_init
	python manage.py runscript auth_init 
