# Name_of_Your_Project

## Setting up

- Using conda

  ```
  # create env
  conda env create --file docker/environment.yml

  # activate it
  conda activate NAMEOFYOURPROJECT

  # install this repo
  (NAMEOFYOURPROJECT) $ pip install -e .
  ```

- Using [docker](https://docs.docker.com/engine/install/ubuntu/)

  Note: Please review [Developing inside Docker Container inside Remote Linux VM](https://bizair.visualstudio.com/Research/_wiki/wikis/Research.wiki/975/Developing-inside-docker-containers-inside-remote-linux-vm).

  ```
  # pull image with [azureml image](https://hub.docker.com/_/microsoft-azureml?tab=description) as base with docker/environment.yml on top
  docker pull commondockerimages.azurecr.io/NAMEOFYOURPROJECT:latest

  # pull image with nvidia pytorch image as base
  # docker pull commondockerimages.azurecr.io/NAMEOFYOURPROJECT:latest-nvidia (for nvidia pytorch base image. See the note below for more details.)

  # run image
  docker run -it --gpus=all -v <PATH_TO_THIS_REPO>:<PATH_TO_THIS_REPO> commondockerimages.azurecr.io/NAMEOFYOURPROJECT:latest

  # setup the repo (run inside the container)
  pip install -e .
  ```

## Running the code
