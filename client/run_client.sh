xhost +
docker build -f Dockerfile . -t test_docker_image
docker run --name test_docker_image --network final_project -e DISPLAY=$DISPLAY --privileged -v /tmp/.X11-unix:/tmp/.X11-unix --rm -ti test_docker_image

