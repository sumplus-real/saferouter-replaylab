DOCKER ?= docker
IMAGE ?= saferouter-replaylab:local
LLM_NAME ?= Apertus-v1.5-8B-Q4_K_M
LLM_BASE_URL ?= http://host.docker.internal:19464
export LLM_NAME LLM_BASE_URL LLM_API_KEY
.PHONY: run build test compare
build:
	$(DOCKER) build -t $(IMAGE) .
run: build
	$(DOCKER) run --rm --name saferouter-replaylab -p 127.0.0.1:19564:19564 -e LLM_NAME -e LLM_BASE_URL -e LLM_API_KEY $(IMAGE)
test:
	python -m unittest discover -s track_2b/tests -v
compare:
	python track_2b/src/evaluate.py
