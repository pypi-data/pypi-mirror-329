import subprocess

from rich.markdown import Markdown
from rich.panel import Panel

from ..utils import console, log_interactions


def hello_world() -> bool:
    console.print(
        Panel(
            Markdown(
                """
## Example: Hello, world

Let's launch a VM, and run the program `echo "Hello, world"`.

This will cost about $0.01.

We'll run this with the following command:

```bash
coiled run --container daskdev/dask:latest echo 'Hello, world'
```

I'll do this here, but you can also do this in another terminal.
""".strip()
            ),
            padding=(0, 3, 1, 3),
        )
    )

    with log_interactions("example-hello-world"):
        subprocess.run(["coiled", "run", "--container", "daskdev/dask:latest", "echo", "'Hello, world'"], check=True)

    return True
