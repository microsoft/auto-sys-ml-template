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

- Using docker

  ```
  # pull image with [azureml image](https://hub.docker.com/_/microsoft-azureml?tab=description) as base with docker/environment.yml on top
  docker pull NAMEOFYOURPROJECT:latest

  # pull image with nvidia pytorch image as base
  # docker pull NAMEOFYOURPROJECT:latest-nvidia

  # run image
  docker run -it --gpus=all -v <PATH_TO_THIS_REPO>:<NAMEOFYOURPROJECT:latest

  # setup the repo (run inside the container)
  pip install -e .
  ```

## Running the code
