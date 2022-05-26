import hydra
from omegaconf import DictConfig


@hydra.main(config_path="configs/", config_name="eval.yaml")
def main(config: DictConfig):

    # Imports can be nested inside @hydra.main to optimize tab completion
    # https://github.com/facebookresearch/hydra/issues/934
    from src import utils
    from src.eval_pipeline import eval

    # Applies optional utilities
    utils.extras(config)

    # Evaluate model
    return eval(config)


if __name__ == "__main__":
    main()
