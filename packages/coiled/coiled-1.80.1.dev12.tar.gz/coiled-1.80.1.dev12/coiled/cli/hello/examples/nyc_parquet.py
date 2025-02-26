from __future__ import annotations

import pathlib
import subprocess

from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax

import coiled

from ..utils import live_panel_print, log_interactions


def nyc_parquet() -> bool | None:
    text1 = Markdown(
        """
## Example: Aggregate 1 TB of Parquet data

There's 1 TB of Parquet data sitting in this S3 bucket:

```
s3://coiled-data/uber/
```

Let's run this Python script to calculate how much Uber/Lyft riders paid vs
how much Uber/Lyft drivers got paid in NYC.\n
"""
    )

    script_basename = "nyc_parquet.py"
    script_path = pathlib.Path(__file__).parent.parent / "scripts" / script_basename
    example_code = Syntax.from_path(str(script_path))

    live_panel_print(text1, Rule(style="grey"), example_code)

    try:
        choice = Prompt.ask(
            "Ready to run this example?",
            # "Would you like me to run this script for you?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
        return False

    if choice == "y":
        with log_interactions("example-nyc-parquet"):
            fill = pathlib.Path(__file__).parent.parent / "scripts" / "fill_ipython.py"
            subprocess.run(["ipython", "-i", fill, str(script_path)], check=True)
    else:
        return None

    return True
