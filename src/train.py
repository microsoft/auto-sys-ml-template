import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../configs/", config_name="train.yaml")
def main(config: DictConfig):
    # Imports can be nested inside @hydra.main to optimize tab completion
    # https://github.com/facebookresearch/hydra/issues/934
    from pipelines.train_pipeline import train

    # Train model
    return train(config)

if __name__ == "__main__":
    main()
