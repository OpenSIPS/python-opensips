NAME ?= pyhton-opensips
OPENSIPS_DOCKER_TAG ?= latest

all: build

.PHONY: build
build:
	docker build \
		--tag="opensips/python-opensips:$(OPENSIPS_DOCKER_TAG)" \
		.
