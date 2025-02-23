from .lineplot import lineplot
from .set_theme import set_theme
import importlib.util

if importlib.util.find_spec("wandb") is not None:
    pass
else:
    print("Warning: `wandb` is not installed. Install with `pip install wandb`.")
