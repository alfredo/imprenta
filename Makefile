build:
	docker-compose run lambda /usr/bin/pip-3.6 install -r /app/pdf/requirements_built.txt -t /app/pdf/vendor/

deploy:
	chalice --project-dir `pwd`/pdf/ deploy --profile sudo

local:
	chalice --debug --project-dir `pwd`/pdf/ local
