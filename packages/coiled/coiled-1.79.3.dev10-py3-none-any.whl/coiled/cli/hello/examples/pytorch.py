from __future__ import annotations

import pathlib
import subprocess

from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax

import coiled

from ..utils import live_panel_print, log_interactions


def pytorch() -> bool | None:
    text1 = Markdown(
        """
## Example: Train a PyTorch model on a GPU

Below we define a PyTorch model and training loop.
We use the Coiled serverless functions decorator to run our
model training function on an NVIDIA A10 GPU on AWS.\n
"""
    )

    script_basename = "pytorch.py"
    script_path = pathlib.Path(__file__).parent.parent / "scripts" / script_basename
    example_code = Syntax.from_path(str(script_path))

    live_panel_print(text1, Rule(style="grey"), example_code)

    try:
        choice = Prompt.ask(
            "Ready to run this example?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
        return False

    if choice == "y":
        with log_interactions("example-pytorch"):
            fill = pathlib.Path(__file__).parent.parent / "scripts" / "fill_ipython.py"
            subprocess.run(["ipython", "-i", fill, str(script_path)], check=True)
    else:
        return None

    return True
