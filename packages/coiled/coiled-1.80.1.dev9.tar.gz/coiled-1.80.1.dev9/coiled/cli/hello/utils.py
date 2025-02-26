import contextlib
import time

import rich
import rich.panel
from rich.console import Console, Group
from rich.live import Live

import coiled
from coiled.utils import error_info_for_tracking

console = Console(width=80)


class Panel(rich.panel.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "padding" not in kwargs:
            self.padding = (1, 2)


@contextlib.contextmanager
def log_interactions(action):
    success = True
    exception = None
    try:
        yield
    except Exception as e:
        # TODO: Better error when something goes wrong in example
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            f"cli-hello:{action}",
            success=success,
            **error_info_for_tracking(exception),
        )


def live_panel_print(*renderables, delay=0.25):
    with Live(
        Panel(renderables[0]),
        console=console,
        auto_refresh=False,
    ) as live:
        for idx in range(len(renderables)):
            time.sleep(delay)
            live.update(Panel(Group(*renderables[: idx + 1]), width=80), refresh=True)
