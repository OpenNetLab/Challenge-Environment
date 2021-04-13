docker_image := chanllenge-env
docker_file := dockers/Dockerfile
docker_container := chanllenge-env
docker_work_dir := /home/vmaf

all: init chanllenge-env

init:
	git submodule init
	git submodule update

chanllenge-env:
	wget https://github.com/OpenNetLab/AlphaRTC/releases/download/20210330.3/alphartc.tar.gz
	docker load -i alphartc.tar.gz

	docker build . --build-arg UID=$(shell id -u) --build-arg GUID=$(shell id -g) -f $(docker_file) -t ${docker_image}

	docker run -itd --name ${docker_container} -w ${docker_work_dir} ${docker_image}
	docker exec -it ${docker_container} /bin/bash -c "cd ${docker_work_dir} && make clean && make install"

