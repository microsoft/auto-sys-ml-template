# Autonomous Systems Research Group: ML Template

This document serves as an onboarding document as well as a template repository to quickstart machine learning experimentation at the Autonomous Systems Research Group at Microsoft.

**Note** Use the table of contents icon <img src="./assets/images/table-of-contents.png" width="25" height="25" /> on the top left corner of this document to get to a specific section quickly.

### Using this template to generate a repository:

- Click on the green colored box titled **Use this template** top right, and name your new repository.
- You can clone your repo when it looks like [example_repo_generated_from_ml_template](https://github.com/AutonomousSystemsResearch/example_repo_generated_from_ml_template).

> **Note** that after you create the template, it will take about **20 seconds** for an automated github action to clean up the generated repository using an auto-commit. Please ensure your repository looks like [example_repo_generated_from_ml_template](https://github.com/AutonomousSystemsResearch/example_repo_generated_from_ml_template) before cloning it.

## Introduction

For the template repository, we will use:

- [Pytorch Lightning](https://pytorch-lightning.readthedocs.io/en/stable/)
  - For minimizing boilerplate code
- [OmegaConf](https://omegaconf.readthedocs.io/)
  - Please go through [OmegaConf's github readme](https://github.com/omry/omegaconf#releases) for tutorials.
  - For config management
    > **Note**: we have an [archived branch called `hydra`](https://github.com/AutonomousSystemsResearch/ml_template/tree/hydra) which uses [hydra](https://hydra.cc/) for config management.
- Logging
  - We primarily use tensorboard. Amulet automatically patches tensorboard scalars to MLFlow for viewing metrics in Azure ML Studio.
- Conda and Docker
  - For development

## Using this repository

### **Running locally**

#### Setup

- **VSCode**

  - Extensions:

    - Hit `Ctrl+Shift+P` and type `Show Recommended Extensions` and install them from the sidebar.
      Or click "yes" when you get a VS Code pop up to install the recommended extensions, which are specified in [.vscode/extensions.json](.vscode/extensions.json).
      Follow [this doc](https://code.visualstudio.com/docs/editor/extension-marketplace#_recommended-extensions) for more details.
    - `Python`, `Pylance`, `Docker`, `GitLens`, `YAML`, and the [Remote development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) are strongly recommended.

  - Debugging:

    - Please follow [VSCode docs and tutorials](https://code.visualstudio.com/docs/python/debugging) on Python debugging
    - A minimal debugging configuration has been provided in [.vscode/launch.json](.vscode/launch.json). Please see VSCode docs on [launch.json configs](https://code.visualstudio.com/docs/python/debugging#_additional-configurations) and [config options](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options).

- **Conda**

  - Recommended for local development and debugging.
  - Note: For CUDA 11.6, see `Creating the conda environment from scratch (click to expand)` below.

  ```
  # create env
  conda env create --file docker/environment.yml

  # activate it
  conda activate ml_template

  # install this repo
  (ml_template) $ pip install -e .

  # install pre-commit (recommended). Scroll down to the #Developing section for details.
  (ml_template) $ pre-commit install
  ```

  > **Note** If you install additional packages in your environment manually, you should update the `environment.yml` correspondingly by doing a `$ conda env export | grep -v "^prefix: " > docker/environment.yml`.

  <details>
      <summary>
      Creating the conda environment from scratch (click to expand)
      </summary>

  ```
  conda update -n base -c defaults conda
  conda create --name ml_template python=3.9
  conda activate ml_template
  conda install pip
  conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
  conda install pytorch-lightning -c conda-forge
  pip install omegaconf \
    pytest \
    sh \
    pre-commit \
    mlflow \
    azureml-mlflow \
    azureml-core \
    torch_tb_profiler \
    opencv-python \
    black isort flake8 \
    psutil \
    rich
  conda env export | grep -v "^prefix: " > docker/environment.yml
  pre-commit install
  pre-commit run --all-files
  pip install -e .
  ```

  For CUDA 11.6:

  ```
  conda update -n base -c defaults conda
  conda create --name ml_template_cu116 python=3.9
  conda activate ml_template_cu116
  conda install pip
  conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge
  pip install pytorch-lightning
  pip install omegaconf \
    pytest \
    sh \
    pre-commit \
    mlflow \
    azureml-mlflow \
    azureml-core \
    torch_tb_profiler \
    opencv-python \
    black isort flake8 \
    psutil \
    rich
  conda env export | grep -v "^prefix: " > docker/environment_cu116.yml
  pre-commit install
  pre-commit run --all-files
  pip install -e .
  ```

  </details>

  <details>
      <summary>
      Upgrading pytorch and cudatoolkit (click to expand)
      </summary>

  ```
  conda remove pytorch torchvision torchaudio cudatoolkit
  # then follow pytorch installation steps, for example:
  conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge
  # then update pytorch lightning:
  pip install pytorch-lightning --upgrade
  pip install pytorch-lightning[extra] --upgrade
  pip install -U jsonargparse[signatures] --upgrade
  ```

  </details>

- **Docker**

  - While submitting jobs to AzureML, we take our local conda environment and overlay them on an appropriate docker base image. For a new project / a custom conda environment, you can build the docker image locally as explained in a note later in this section. Optionally, the docker image building can be automated by CI (as explained later) if your project has a frequently update conda environment.

  - For `ml_template`, we have [three docker images](docker/) built automatically on each commit to `main` branch or a branch corresponding to a Pull Request.
    Docker images are pushed to [PRIVATEAZURECONTAINERREGISTRYNAME](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/964a24a8-8835-43c1-9633-7d78841facf1/resourceGroups/research_team/providers/Microsoft.ContainerRegistry/registries/PRIVATEAZURECONTAINERREGISTRYNAME/repository) container registory under [ml_template](https://ms.portal.azure.com/#view/Microsoft_Azure_ContainerRegistries/RepositoryBlade/id/%2Fsubscriptions%2F964a24a8-8835-43c1-9633-7d78841facf1%2FresourceGroups%2Fresearch_team%2Fproviders%2FMicrosoft.ContainerRegistry%2Fregistries%25PRIVATEAZURECONTAINERREGISTRYNAME/repository/ml_template).
    To automate this for your generated repository from this template, please follow make an Azure Pipelines which will `azure-pipelines.yml`

  - The following tags correspond to the the *latest commit on the main branch.*

|                      Tag                      |                        Dockerfile                         |                                  docker pull command                                  |                                                                                       Base Image                                                                                       |
| :-------------------------------------------: | :-------------------------------------------------------: | :-----------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|         `latest`  or `latest-azureml`         |         [azureml](docker/Dockerfile_base_azureml)         |     `docker pull PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest`     | [mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04:latest](https://github.com/Azure/AzureML-Containers/tree/master/base/gpu/openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04) |
| `latest-nightly`  or `latest-azureml-nightly` | [azureml_nightly](docker/Dockerfile_base_azureml_nightly) | `docker pull PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-nightly` | [mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04:latest](https://github.com/Azure/AzureML-Containers/tree/master/base/gpu/openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04) |
|                `latest-nvidia`                |          [nvidia](docker/Dockerfile_base_nvidia)          | `docker pull PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-nvidia`  |                                  [nvcr.io/nvidia/pytorch:22-06-py3](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/index.html)                                  |

- Building docker images and running docker containers locally - can be useful to reproduce issues which might occur while submitting to AzureML on your local machine. Please peruse public documentation on docker + vscode.

```
# pull image with [azureml image](https://hub.docker.com/_/microsoft-azureml?tab=description) as base with docker/environment.yml on top
docker pull PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest

# (optional) pull image with nvidia pytorch image as base
docker pull PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-nvidia (for nvidia pytorch base image. See the note below for more details.)

# run image
docker run -it --gpus=all -v <PATH_TO_THIS_REPO>:<PATH_TO_THIS_REPO> PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest

# (optional) recommended give a name to your container
docker run -it --rm --name=MYFANCYCONTAINERNAME --gpus=all -v <PATH_TO_THIS_REPO>:<PATH_TO_THIS_REPO> PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest

# setup the repo (run inside the container)
pip install -e .

# install pre-commit (recommended). Scroll down to the "Developing" section for details.
pre-commit install
```

<details>
  <summary>
  More details on docker image tags for Pull Request and main branch builds (click to expand)
  </summary>
Similar to the `main` branch, for each pull request, we have:

- `PR-<#pr_number>-latest` aka `PR-<pr_number>-latest-azureml`
- `PR-<#pr_number>-latest-nightly` aka `PR-<pr_number>-latest-azureml-nightly`
- `PR-<#pr_number>-latest-nvidia`

And finally for both `main` and PR branches, we have tags corresponding to git commit hashes

- `main-<gitcommithash>-azureml` and `PR-<pr_number>-<gitcommithash>-azureml`
- `main-<gitcommithash>-azureml-nightly` and `PR-<pr_number>-<gitcommithash>-azureml-nightly`
- `main-<gitcommithash>-nvidia` and `PR-<pr_number>-<gitcommithash>-nvidia`

For example:

- `main-7fadad2b-azureml`, `main-7fadad2b-azureml-nightly`, `main-7fadad2b-nvidia`: correspond to [commit 7fadad2b](https://github.com/AutonomousSystemsResearch/ml_template/commit/7fadad2b1391cdbbc46422a6865caaf0300b9af8) on `main` branch with our three different dockerfiles
- `PR-50-latest-azureml`, `PR-50-latest-azureml-nightly`, `PR-50-latest-nvidia`: correspond to latest commit on [PR#50](https://github.com/AutonomousSystemsResearch/ml_template/pull/50) with our three different dockerfiles
- `PR-50-eef3b90-azureml`, `PR-50-eef3b90-azureml-nightly`, `PR-50-eef3b90-nvidia`: correspond to [commit eef3b90](https://github.com/AutonomousSystemsResearch/ml_template/pull/50/commits/eef3b900fc956614c7d45eac6fa9245b57f7bd72) on [PR#50](https://github.com/AutonomousSystemsResearch/ml_template/pull/50) with our three different dockerfiles

</details>
<details>
    <summary>
    Building and understanding our Dockerfiles (click to expand)
    </summary>

- We have three docker files:

  - azureml base:
    - [docker/Dockerfile_base_azureml](docker/Dockerfile_base_azureml)
    - [docker/Dockerfile_base_azureml_latest](docker/Dockerfile_base_azureml_latest)
  - nvidia pytorch base:
    - [docker/Dockerfile_base_nvidia](docker/Dockerfile_base_nvidia).

- Both of the azureml base images grabs a base image from [here](https://github.com/Azure/AzureML-Containers/tree/master/base/gpu), and put the user's conda environment ([docker/environment.yml](docker/environment.yml)) on top of the base page.

- In the `latest-azureml` version, packages in your local conda environment should match the docker image exactly.

- In the `latest-azureml-nightly` image, pytorch (including cudatoolkit) and pytorch lightning are updated to the nightly versions.

- The nvidia pytorch base image grabs a base image from [here](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch/tags) ([here](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/index.html) for details), which already has the latest version of pytorch.
  Instead of using user's conda environment, this docker file uses `pip` to install pytorch lightning and other dependencies on top of base image. So this image can have different versions of  packages as compared to your conda environment.

All docker images accept a build argument to update the base image version easily:

- azureml images:
  - take base azure image name's suffix **and** tag. see available options [here](https://github.com/Azure/AzureML-Containers/tree/master/base/gpu):
    - examples: `openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04:latest`, `openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04:latest`, and so on.
- nvidia pytorch image:
  - takes base nvidia image name's tag only.
  - see [available tags here](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch/tags) and [the release notes for their contents](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/index.html)
  - examples: `22.06-py3`, `22.05-py3`, and so on.

Please review the arguments in the dockerfiles carefully. These can also be seen by reading through [azure-pipelines.yml](azure-pipelines.yml).

Building the azure-ml base + conda env images locally:

```
cd docker;

docker build \
  -f Dockerfile_base_azureml \
  --build-arg BASE_IMAGE=openmpi4.1.0-cuda11.3-cudnn8-ubuntu20.04:latest \
  -t PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-azureml .

# note that in the PRIVATEAZURECONTAINERREGISTRYNAME acr, latest is equivalent to latest-azureml tag. So, we can just re-tag the image:
docker tag PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-azureml PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest
```

For the CUDA 11.6 version:

```
cd docker;

docker build \
  -f Dockerfile_base_azureml_cu116 \
  --build-arg BASE_IMAGE=openmpi4.1.0-cuda11.6-cudnn8-ubuntu20.04:latest \
  -t PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-azureml-cu116 .

# note that in the PRIVATEAZURECONTAINERREGISTRYNAME acr, latest is equivalent to latest-azureml tag. So, we can just re-tag the image:
docker tag PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-azureml-cu116 PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-cu116
```

Building the nvidia-pytorch image locally:

```
# building nvidia-pytorch image with locally.
cd docker;

docker build \
  -f Dockerfile_base_nvidia \
  --build-arg BASE_IMAGE=22.06-py3 \
  -t PRIVATEAZURECONTAINERREGISTRYNAME.azurecr.io/ml_template:latest-nvidia .
```

</details>

<details>
    <summary>
    Developing inside docker containers with VSCode: (click to expand)
    </summary>

- [Attach to a docker container](https://code.visualstudio.com/docs/remote/attach-container)

- [Devcontainer](https://code.visualstudio.com/docs/remote/containers)

  > **Note**: This method can be used on an Azure VM or locally with no change and uses docker

  Follow the steps below:

  - Connect to your remote Azure VM using VS Code
  - Open the workspace within a docker container for development, either using the popup as shown in the animation above, or by searching for `(Re)Build and (Re)open in container` in the  command palette (hit `Ctrl+Shift+P` to open the command palette)
  - After setup is complete, it is time to set up the repository:
    ```
      pip install -e .
      pre-commit install
    ```
  - > **Note**: By default, the devcontainer uses the [azureml-conda base image](docker/Dockerfile_base_azureml). We can also use the [nvidia base image](docker/Dockerfile_base_nvidia) by modifying the `dockerfile` line in [devcontainer.json](.devcontainer/devcontainer.json). Similarly, we can edit the docker files build argument therein itself.

</details>

#### Running MNIST example

- Understanding OmegaConf and config files

  - Please review OmegaConf's [github readme](https://github.com/omry/omegaconf#releases) for [their documentation](https://omegaconf.readthedocs.io/en/2.2_branch/), [slides (for ver 2.1)](https://docs.google.com/presentation/d/e/2PACX-1vT_UIV7hCnquIbLUm4NnkUpXvPEh33IKiUEvPRF850WKA8opOlZOszjKdZ3tPmf8u7hGNP6HpqS-NT5/pub?start=false&loop=false&delayms=3000&slide=id.p), and a [live tutorial](https://github.com/omry/omegaconf#live-tutorial).

- Single GPU

  ```
  python src/train.py base=configs/train.yaml trainer.num_nodes=1 trainer.devices=1
  ```

- Multiple GPUs

  ```
  python src/train.py base=configs/train.yaml trainer.num_nodes=1 trainer.devices=4
  ```

### Running on Azure

Note: This section used internal tools for job submission to Azure ML workspaces. This section is not supported publicly at the time of writing. However, one may peruse existing public documentation on azure ml.

### Developing

#### Tests

The template has some basic tests in `tests/` directory. To run them, run:

```
# run all tests
pytest

# run single test
pytest tests/test_dev_fast_run.py
```

List of tests implemented:

- [fast_dev_run](https://pytorch-lightning.readthedocs.io/en/stable/common/debugging.html#fast-dev-run):  a simple check to run your trainer on single batch of train, valid, and test datase.
  It can also be useful to quickly check your code works by running while adding new features:
  ```
  python src/train.py base=configs/train.yaml --fast_dev_run=True
  ```

#### Code formatting and Linting

We use:

- [black](https://black.readthedocs.io/en/stable/) for code formatting

- [isort](https://pycqa.github.io/isort/) for import ordering

- [pycln](https://hadialqattan.github.io/pycln/#/) for removing unused imports

- Running locally:

  ```
  $ cd ml_template;
  $ black .
  $ isort .
  $ pycln --all .
  ```

#### Pre-commit Hooks: Automating Code formatting and Linting

[pre-commit](https://pre-commit.com/) hooks automate black autoformatting and ensuring PEP8 compliance.

- Setting up:

  ```
  $ cd ml_template;
  $ pre-commit install
  ```

- Running:

  After the above step, `pre-commit` will run **automatically** when you `git commit`.
  If the run fails with errors in red, you can check the edits made by `pre-commit` by `git diff`.
  If the changes look good, (1) `git add` those files again, and then (2) run `git commit` again.

  Optionally, you can also run pre-commit manually by:

  ```
  $ pre-commit run --all-files
  ```

- Updating hooks:
  Use the `autoupdate` command to keep the versions of formatters in `.pre-commit-config.yaml` up to date.

  ```
  $ pre-commit autoupdate
  ```

### Continuous Integration

- **Github Actions**

  - [Pre-commit checks](.github/workflows/pre-commit.yml)
  - [Template cleanup](.github/workflows/template-cleanup.yml):
    When a new repository is generated using this template, this action replace `README.md` with `README_template.md` to keep microsoft links internal.

- **Azure Pipelines**

  - Create an azure devops pipeline for your repository.
    This automates building of your docker images, and also run pytests on them.

  - The azure pipeline logs can be seen at Azure DevOps webpage, but not on with github UI directly.

    Pull Request example:

    - You can click `View more details on Azure Pipelines` under the `Checks` section of a github PR.
    - See [PR#6/checks](https://github.com/AutonomousSystemsResearch/ml_template/pull/6/checks) for an example.

    <br>

  - [Docker Build and Push Image](azure-pipelines.yml)

    See the job `BuildDockerImageAndPush` in [azure-pipelines.yml](azure-pipelines.yml). It will build the image in [docker/Dockerfile](docker/Dockerfile) and push it to a private azure container registry

    See docker section under #running-locally for details

### Contributing

- conda `environment.yml` update:

  If you install packages in conda, update the `docker/environment.yml` by `conda env export | grep -v "^prefix: " > docker/environment.yml`, and send a PR.

## Reference Repositories

- Pytorch Lightning:

  - Pytorch v/s Pytorch Lightning

    - [PyTorch Lightning for Dummies - A Tutorial and Overview
      ](https://www.assemblyai.com/blog/pytorch-lightning-for-dummies/)
    - [PyTorch Lightning: DataModules, Callbacks, TPU, and Loggers
      ](https://dev.to/krypticmouse/pytorch-lightning-datamodules-callbacks-tpu-and-loggers-4nhb)

  - Template / reference repositories

    - https://github.com/ashleve/lightning-hydra-template
    - https://github.com/lkhphuc/lightning-hydra-template
    - [Pytorch lightning bolts](https://lightning-bolts.readthedocs.io/en/latest/)
      - Look inside the code for datamodules, datasets, models, etc: https://github.com/PyTorchLightning/lightning-bolts/tree/master/pl_bolts

- Pytorch Geometric:

  - [lightning-examples](https://github.com/pyg-team/pytorch_geometric/tree/d451d6d20287b03cbe5036e5c53ee5f633f3c429/examples/pytorch_lightning)
  - [torch_geometric.data.lightning_datamodule](https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/data/lightning_datamodule.html)
  - [Graph Gym](https://pytorch-geometric.readthedocs.io/en/latest/notes/graphgym.html)

- Pytorch data, datapipes, dataloaders:

  - https://pytorch.org/data/main/examples.html
  - https://github.com/tcapelle/torchdata
  - https://github.com/pytorch/data
