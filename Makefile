docker_image := chanllenge-env
docker_file := dockers/Dockerfile

all: chanllenge-env

chanllenge-env:
	wget https://github.com/OpenNetLab/AlphaRTC/releases/latest/download/alphartc.tar.gz
	docker load -i alphartc.tar.gz
	docker build . --build-arg UID=$(shell id -u) --build-arg GUID=$(shell id -g) -f $(docker_file) -t ${docker_image}

