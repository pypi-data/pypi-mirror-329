#!/usr/bin/env python3
"""
odrive_can CLI
"""

import json
import logging
import os
import subprocess
from pathlib import Path

import click
import coloredlogs  # type: ignore

from odrive_can import LOG_FORMAT, TIME_FORMAT
from odrive_can.utils import run_main_async

log = logging.getLogger()
coloredlogs.install(level="INFO", fmt=LOG_FORMAT, datefmt=TIME_FORMAT)

# pylint: disable=import-outside-toplevel, unused-argument, broad-except

# ------------------ helpers


@click.group()
def cli():
    pass  # pragma: no cover


@cli.group()
def demo():
    """demonstration of control modes"""


@cli.command()
def info():
    """Print package info"""
    from odrive_can import __version__

    print(__version__)


@cli.command()
@click.option("--axis-id", default=0, help="ODrive axis ID")
def mock(axis_id):
    """Mock ODrive CAN interface"""
    from .mock import main

    main(axis_id=axis_id)


@cli.command()
def inspect():
    """Inspect and decode ODrive CAN messages"""
    from .inspector import main

    main()


@cli.command()
@click.option(
    "--output-file",
    default="odrive_config.json",
    help='The name of the output file (default: "odrive_config.json")',
)
def backup(output_file):
    """Backup config to config folder"""
    tmp_path = Path("/tmp")
    odrive_files = tmp_path.glob("odrive*")

    # 1. Remove all /tmp/odrive* files
    for file in odrive_files:
        file.unlink()
        print(f"Removed: {file}")

    # 2. Run `odrivetool backup-config`
    try:
        result = subprocess.run(
            "odrivetool backup-config",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=5,
        )
        if result.returncode != 0:
            print("Failed to run 'odrivetool backup-config'")
            print(result.stderr.decode())
            return
    except subprocess.TimeoutExpired:
        print("Failed to run 'odrivetool backup-config'")
        print("Timeout expired")
        return

    # 3. Find the generated `odrive-config-*.json` file and read it
    config_files = list(tmp_path.glob("odrive-config-*.json"))
    if not config_files:
        print("No config file found")
        return

    config_file = max(config_files, key=os.path.getctime)  # Get the latest file
    data = config_file.read_text()

    # 4. Save parsed data using json, with human readable formatting
    parsed_data = json.loads(data)

    # Save the formatted data to the 'config' directory
    dest = Path(output_file)
    with dest.open("w", encoding="utf8") as f:
        json.dump(parsed_data, f, indent=2)
    print(f"Formatted config saved to {dest}")


@demo.command()
@click.option("--axis-id", default=1, help="ODrive axis ID")
@click.option("--amplitude", default=40, help="Amplitude")
@click.option(
    "--input-mode",
    type=click.Choice(["POS_FILTER", "TRAP_TRAJ"], case_sensitive=False),
    default="POS_FILTER",
    help="Input mode (POS_FILTER or TRAP_TRAJ)",
)
def position(axis_id, input_mode, amplitude):
    """Position control demo"""
    from .examples.position_control import main

    try:
        run_main_async(main(axis_id, input_mode, amplitude))
    except Exception as e:
        log.error(e)


@demo.command()
@click.option("--axis-id", default=1, help="ODrive axis ID")
@click.option("--amplitude", default=40, help="Amplitude")
def velocity(axis_id, amplitude):
    """Velocity control demo"""
    from .examples.velocity_control import main

    try:
        run_main_async(main(axis_id, amplitude))
    except Exception as e:
        log.error(e)


@demo.command()
@click.option("--axis-id", default=1, help="ODrive axis ID")
@click.option("--amplitude", default=40, help="Amplitude")
def watchdog(axis_id, amplitude):
    """Demonstrate the watchdog feature"""
    from .examples.watchdog import main

    try:
        run_main_async(main(axis_id, amplitude))
    except Exception as e:
        log.error(e)


if __name__ == "__main__":
    cli()  # pragma: no cover
