build:
	bin/bootstrap

deploy:
	chalice --project-dir `pwd`/pdf/ deploy

local:
	chalice --debug --project-dir `pwd`/pdf/ local
