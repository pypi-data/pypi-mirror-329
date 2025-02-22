import asyncio
from typing import List

from absl import app, flags, logging
from elgato import Elgato, State
from elgato.exceptions import ElgatoConnectionError

FLAGS = flags.FLAGS

_LIGHTS = flags.DEFINE_multi_string(
    "light", None, "Light to toggle. Repeat for multiple."
)


async def main() -> None:
    """Toggle lights."""
    if _LIGHTS.value:
        lights: List[str] = _LIGHTS.value
        await asyncio.gather(*[toggle(light) for light in lights])
    else:
        logging.error("No lights provided, use --light flag(s) to provide hostnames.")


async def toggle(hostname: str) -> None:
    """Toggle a single light."""

    async with Elgato(hostname) as elgato:
        try:
            state: State = await elgato.state()
            await elgato.light(on=(not state.on))
        except ElgatoConnectionError as e:
            logging.error(f"{e}: {hostname}")


def run_async(argv) -> None:
    del argv
    asyncio.run(main())


def run() -> None:
    app.run(run_async)


if __name__ == "__main__":
    run()
