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

- VSCode + Docker

  - [Using Devcontainer](https://code.visualstudio.com/docs/remote/containers)

    - Connect to your remote Azure VM using VS Code

    - Open the workspace within a docker container for development, either using the popup as shown in the animation above, or by searching for `(Re)Build and (Re)open in container` in the  command palette (hit `Ctrl+Shift+P` to open the command palette)

    - After setup is complete, it is time to set up the repository:

      ```
        pip install -e .
        pre-commit install
      ```

    - Note: By default, the devcontainer uses the [azureml-conda base image](docker/Dockerfile_base_conda). We can also use the [nvidia base image](docker/Dockerfile_base_nvidia) by modifying the `dockerfile` line in [devcontainer.json](.devcontainer/devcontainer.json). Similarly, we can edit the docker files build argument therein itself.

  - [Attach to a docker container](https://code.visualstudio.com/docs/remote/attach-container)

## Running the code
