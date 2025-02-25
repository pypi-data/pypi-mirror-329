from __future__ import annotations

import asyncio
import functools
import json
import subprocess
import sys

import dask
import dask.config
import httpx
import importlib_metadata
from rich import box, print
from rich.console import Group
from rich.markdown import Markdown
from rich.prompt import Prompt

import coiled
from coiled.pypi_conda_map import PYPI_TO_CONDA
from coiled.scan import scan_prefix
from coiled.utils import error_info_for_tracking, login_if_required

from .examples import examples
from .utils import Panel, console, log_interactions


def get_dependencies():
    # Full list of dependencies (on PyPI)
    return [
        "coiled",
        "dask",
        "pandas",
        "bokeh",
        "s3fs",
        "ipython",
        "matplotlib",
        "torch",
        "torchvision",
        "xarray",
        "zarr",
    ]


def get_conda_dependencies():
    deps = get_dependencies()
    if "dask" in deps:
        # These are included with `dask` on conda-forge
        deps = [d for d in deps if d not in ("pandas", "bokeh")]
    deps = [PYPI_TO_CONDA.get(p, p) if p not in ("dask", "matplotlib") else p for p in deps]
    return deps


def needs_login():
    if dask.config.get("coiled.token", False) is False:
        # Need login if no token
        return True

    token = dask.config.get("coiled.token")
    # Manually hitting this endpoint to avoid implicitly triggering the login flow
    r = httpx.get("https://cloud.coiled.io/api/v2/user/me", headers={"Authorization": f"ApiToken {token}"})
    if r.is_success:
        return False
    else:
        # Need login if invalid token
        return True


def get_interactions():
    response = subprocess.check_output(["coiled", "curl", "/api/v2/interactions/user-interactions/hello"])
    return json.loads(response, strict=False)


def get_alread_run_examples():
    already_run = dict.fromkeys(examples.keys(), False)
    interactions = get_interactions()
    for i in interactions:
        if i["action"].startswith("cli-hello:example-") and i["action"] != "cli-hello:example-exit" and i["success"]:
            name = i["action"].split(":")[1][len("example-") :]
            already_run[name] = True
    return already_run


def do_hello_wizard() -> bool:
    console.print(
        Panel(
            r"""
[bold]                                                  [rgb(0,95,255)]                ..       [/]
                                                   [rgb(0,95,255)]               ###      [/]
              ____           _   _              _  [rgb(0,95,255)]          .### ###.     [/]
             / ___|   ___   (_) | |   ___    __| | [rgb(0,95,255)]         .#### .#.      [/]
            | |      / _ \  | | | |  / _ \  / _` | [rgb(0,95,255)]         #####          [/]
            | |___  | (_) | | | | | |  __/ | (_| | [rgb(0,95,255)]         .#### .        [/]
             \____|  \___/  |_| |_|  \___|  \__,_| [rgb(0,95,255)]           .## ###      [/]
                                                   [rgb(0,95,255)]               ###.     [/]
                 Website: [rgb(0,95,255)][link=https://coiled.io?utm_source=coiled-hello&utm_medium=banner]https://coiled.io[/link][/rgb(0,95,255)]        [rgb(0,95,255)]             # ###      [/]
                 Docs: [rgb(0,95,255)][link=https://docs.coiled.io?utm_source=coiled-hello&utm_medium=banner]https://docs.coiled.io[/link][/rgb(0,95,255)]      [rgb(0,95,255)]            ## ##.      [/]
                                                   [rgb(0,95,255)]            ##          [/]
                                                   [rgb(0,95,255)]             #          [/][/bold]
""".strip()  # noqa
        )
    )

    do_login = needs_login()
    token_text = ""
    if do_login:
        token_text = (
            "Our first step will send you to [link=https://cloud.coiled.io]cloud.coiled.io[/link], "
            "have you make a free account, and download an API token."
        )

    # Here, and in a few other places, we need to be careful to not run code
    # like `coiled.add_interaction` that triggers the login flow implicitly.
    # We want to present the user with the welcome prompt first, so they know
    # what to expect -- then do the login flow if needed.
    if do_login:
        already_run = dict.fromkeys(examples.keys(), False)
    else:
        already_run = get_alread_run_examples()

    software_checks = [has_mixed_conda_channels, has_macos_system_python, has_missing_dependencies]
    software_ready = not any([check() for check in software_checks])

    console.print(
        Panel(
            Group(
                "[bold underline]Welcome![/bold underline]\n",
                Markdown(
                    f"""
Welcome to Coiled, a lightweight cloud computing platform!

To start we'll go through these steps:

1. {"✅ " if not do_login else ""}Login to Coiled
2. {"✅ " if already_run["hello-world"] else ""}Run "Hello, world"
3. {"✅ " if software_ready else ""}Install Python libraries
4. Choose larger examples to run like:
    - Process 1 TB of Parquet data
    - Train a PyTorch model on a GPU
    - Churn through 2 TB of geospatial data
    - And more...

{token_text}
""".strip()
                ),
            )
        )
    )

    try:
        choice = Prompt.ask(
            "Good to go?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        if not do_login:
            coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    if not do_login:
        coiled.add_interaction("cli-hello:ready-start", success=True, choice=choice)

    if choice == "n":
        print("See you next time :wave:")
        return True

    # Handle login if needed
    if do_login:
        with log_interactions("login"):
            asyncio.run(login_if_required())
            console.print(
                Panel(
                    "[green]Great! You're logged in with Coiled. Let's go run some jobs[/green] :thumbsup:",
                    border_style="green",
                    title="Coiled login",
                )
            )
    else:
        console.print(
            Panel(
                "[green]You've already logged into Coiled. Good job![/green] :thumbsup:",
                border_style="green",
                title="Coiled login",
            )
        )

    # Run "Hello world" if needed
    if already_run["hello-world"]:
        console.print(
            Panel(
                "[green]I see you've already run 'Hello, world' too! Onto bigger examples...[/green] :rocket:",
                border_style="green",
                title="Hello, world",
            )
        )
    else:
        examples["hello-world"]()
        console.print(
            Panel(
                "Let's try another example...",
                border_style="green",
                title="More examples",
            )
        )

    # Software environment setup
    if software_ready:
        console.print(
            Panel(
                "[green]You've got all the right Python packages installed[/green] :white_check_mark:",
                border_style="green",
                title="Install Python packages",
            )
        )
    else:
        for check in [messy_software_message, missing_dependencies_message]:
            result = check()
            if result is True:
                return True
            elif result is False:
                return False

    # Display examples
    run_example = True
    while run_example is not False:
        run_example = examples_prompt()
    return True


def examples_prompt() -> bool | None:
    # We nudge folks to run the "Hello, world" example first

    already_run = get_alread_run_examples()
    if already_run["hello-world"]:
        hello_world_option = '"Hello, world"'
        start_simple_text = ""
    else:
        hello_world_option = '[green]"Hello, world" (recommended)[/green]'
        start_simple_text = "I recommend starting simple."

    console.print(
        Panel(
            Group(
                "[bold underline]Examples[/bold underline] :tada:\n",
                Markdown(
                    f"""
To start, try one of these simple calculations

1. {"✅ " if already_run["hello-world"] else ""}Run a script: {hello_world_option}
2. {"✅ " if already_run["nyc-parquet"] else ""}Dask at scale: Aggregate 1 TB of parquet data
3. {"✅ " if already_run["xarray-nwm"] else ""}Xarray at scale: Aggregate 2 TB of geospatial data
4. {"✅ " if already_run["pytorch"] else ""}Serverless functions: Train a PyTorch model on a GPU
5. Exit

{start_simple_text}
"""  # noqa: E501,
                ),
            )
        )
    )

    choices = list(map(str, range(1, len(examples.keys()) + 1)))
    # Have default be the first non-run example, excluding the last "exit" option
    default = "1"
    for idx, value in enumerate(list(already_run.values())[:-1], start=1):
        if value is False:
            default = str(idx)
            break

    try:
        choice = Prompt.ask(
            "What would you like to try?",
            choices=choices,
            default=default,
            show_choices=True,
            show_default=True,
        )
        choice = int(choice)
        coiled.add_interaction("cli-hello:examples-prompt", success=True, choice=list(examples.keys())[choice - 1])
    except KeyboardInterrupt:
        coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    example = list(examples.values())[choice - 1]
    result = example()
    if result is True:
        # TODO: Once hosted exists, give option to run cloud setup
        console.print(
            Panel(
                "\n[green]Let's try another example...[/green]\n",
                border_style="green",
                title="More examples",
            )
        )

    return result


@functools.cache
def cached_scan():
    return asyncio.run(scan_prefix())


def has_mixed_conda_channels():
    scan = cached_scan()
    return any(pkg for pkg in scan if pkg["channel"] != "conda-forge" and pkg["source"] == "conda")


def has_macos_system_python():
    return sys.platform == "darwin" and "Python3.framework" in sys.exec_prefix


def messy_software_message():
    msg_mixed_channels = ""
    if has_mixed_conda_channels():
        msg_mixed_channels = "has packages from multiple conda channels"

    msg_system_macos = ""
    if has_macos_system_python():
        msg_system_macos = "is using the macOS system Python"

    recommendation = ""
    if msg_mixed_channels or msg_system_macos:
        dependencies = get_conda_dependencies()
        formatted_dependencies = " \\\n\t".join(dependencies)
        if msg_mixed_channels:
            recommendation = f"""I notice you have conda installed. Making a new environment is easy.

```bash
conda create -n coiled -c conda-forge -y {formatted_dependencies}
conda activate coiled
coiled hello
```

I recommend quitting this wizard (Ctrl-C) and running the commands above.\n
"""
        else:
            recommendation = f"""Making a new environment with conda is easy.

```bash
curl -L -O \\
    "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
conda create -n coiled -c conda-forge -y {formatted_dependencies}
conda activate coiled
coiled hello
```

I recommend quitting this wizard (Ctrl-C) and running the commands above.\n
"""

        console.print(
            Panel(
                Markdown(
                    f"""
We're about to run some fun Python examples.
But, this Python environment {msg_mixed_channels or msg_system_macos},
which makes it kinda messy.

Normally, Coiled copies your local environment to the cloud machines (no Docker!)
I'm not confident we'll be able to copy an environment this messy though.

You have some options:
-  Make a fresh and clean virtual environment (recommended!)
-  Use your own Docker image (but only if you love docker)
-  Try anyway!

""".strip()  # noqa
                ),
                # padding=(1, 1),
                title="Whoa! Messy Python environment",
                border_style="blue",
            )
        )
        # Printing this in a separate panel without a border so the user
        # can copy multline code snippets directly into their terminal
        # (otherwise the "|" characters in the panel border are copied as well :/)
        console.print(Panel(Markdown(recommendation), box=box.SIMPLE))
        try:
            choice = Prompt.ask(
                "Proceed anyway?",
                choices=["y", "n"],
                default="n",
                show_choices=True,
            )
        except KeyboardInterrupt:
            coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
            return False

        coiled.add_interaction("cli-hello:messy-software-continue", success=True, choice=choice)
        if choice == "y":
            # Continue with wizard
            return None
        else:
            console.print("See you in a minute with that new software environment :wave:")
            return True
    else:
        return None


def has_missing_dependencies():
    dependencies = get_dependencies()
    missing = []
    for dep in dependencies:
        try:
            importlib_metadata.distribution(dep)
        except ModuleNotFoundError:
            missing.append(dep)
    return bool(missing)


def missing_dependencies_message():
    dependencies = get_dependencies()
    missing = []
    for dep in dependencies:
        try:
            importlib_metadata.distribution(dep)
        except ModuleNotFoundError:
            missing.append(dep)

    if missing:
        if len(missing) > 5:
            missing_formatted = " \\\n\t".join(missing)
        else:
            missing_formatted = " ".join(missing)
        console.print(
            Panel(
                Markdown(
                    f"""
Heads up!
You're missing some dependencies for the examples we're about to run.

These examples use libraries like `pandas`, `torch`, `xarray`, and `s3fs`.\n
You don't need all of these libraries but some of the examples won't work without them.

Want me to install the others right now with this command?

```bash
python -m pip install {missing_formatted}
```
""".strip()  # noqa
                ),
                title="Missing dependencies",
                border_style="yellow",
            )
        )

        try:
            choice = Prompt.ask(
                "Run pip command?",
                choices=["y", "n"],
                default="y",
                show_choices=True,
            )
        except KeyboardInterrupt:
            coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
            return False

        coiled.add_interaction("cli-hello:install-missing-deps", success=True, choice=choice)
        if choice == "y":
            success = True
            exception = None
            try:
                subprocess.run(["python", "-m", "pip", "install", *missing])
            except Exception as e:
                # TODO: Better handling when things go wrong
                success = False
                exception = e
                raise e
            finally:
                coiled.add_interaction(
                    "cli-hello:missing-deps-installed",
                    success=success,
                    packages=missing,
                    **error_info_for_tracking(exception),
                )

            console.print(
                Panel(
                    "[green]\nYou've got all the right Python packages installed[/green] :white_check_mark:\n",
                    border_style="green",
                    title="Install Python packages",
                )
            )

            # Continue with wizard
            return None
        else:
            # Continue with wizard
            return None
    else:
        return None
