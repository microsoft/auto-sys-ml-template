import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../configs/", config_name="eval.yaml")
def main(config: DictConfig):
    # Imports can be nested inside @hydra.main to optimize tab completion
    # https://github.com/facebookresearch/hydra/issues/934
    from pipelines.eval_pipeline import eval

    # Evaluate model
    return eval(config)


if __name__ == "__main__":
    main()
