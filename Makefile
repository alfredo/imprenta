build:
	bin/bootstrap

deploy:
	chalice --project-dir `pwd`/pdf/ deploy --profile sudo

local:
	chalice --debug --project-dir `pwd`/pdf/ local
