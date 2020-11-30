# Docker Repo Cache Data generator

This is a Proof of Concept (PoC) implementation of updating the docker clients cache of data about registry/repository layers. This cache is used to determine when to push a layer or first check the registry if the layer exists and if it doesn't only then push. This is a workaround to the fact that the docker client will automatically push all layers without checking a repository on a first push.

## Installation
Install the requirements from the requirements.txt in you're preferred manner, such as a virtualenv.

## Usage
```bash
AWS_DEFAULT_REGION=us-west-2 REPO_NAME=test IMAGE_TAG=mytag REGISTRY_URL='XXXXXX.dkr.ecr.us-west-2.amazonaws.com' python3 main.py
```
