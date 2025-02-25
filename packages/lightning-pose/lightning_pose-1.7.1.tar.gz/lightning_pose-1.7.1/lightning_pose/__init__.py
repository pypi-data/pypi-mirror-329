__version__ = "1.7.1"

from pathlib import Path

from omegaconf import OmegaConf

LP_ROOT_PATH = (Path(__file__).parent.parent).absolute()
OmegaConf.register_new_resolver("LP_ROOT_PATH", lambda: LP_ROOT_PATH)
