import os

import click

from artefacts.cli.constants import DEFAULT_API_URL
from artefacts.cli.utils import config_validation, read_config
from artefacts.cli.containers.utils import ContainerMgr


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def containers(ctx: click.Context, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug


@containers.command()
@click.option(
    "--path",
    default=".",
    help="Path to the root of the project, where a Dockerfile is available.",
)
@click.option(
    "--dockerfile",
    default="Dockerfile",
    help="File name of the container definition file. Defaults to the standard Dockerfile inside the project root (see --path)",
)
@click.option(
    "--name",
    required=False,
    help="Name for the generated container",
)
@click.pass_context
def build(ctx: click.Context, path: str, dockerfile: str, name: str):
    if not os.path.exists(os.path.join(path, dockerfile)):
        raise click.ClickException(
            f"No {dockerfile} found here. I cannot build the container."
        )
    if name is None:
        name = "artefacts"
    handler = ContainerMgr()
    image, _ = handler.build(path=path, name=name)
    print(f"Package complete in image: {image}")


@containers.command()
@click.argument("name")
@click.pass_context
def check(ctx: click.Context, name: str):
    if name is None:
        name = "artefacts"
    handler = ContainerMgr()
    result = handler.check(name)
    if ctx.parent is None:
        # Print only if the command is called directly.
        print(f"Package {name} exists and ready to use.")
    return result


@containers.command()
@click.argument("image")
@click.argument("jobname")
@click.option(
    "--config",
    callback=config_validation,
    default="artefacts.yaml",
    help="Artefacts config file.",
)
@click.option(
    "--with-gui",
    "with_gui",
    default=False,
    help="Show any GUI if any is created by the test runs. By default, UI elements are run but hidden---only test logs are returned. Please note GUI often assume an X11 environment, typically with Qt, so this may not work without a appropriate environment.",
)
@click.pass_context
def run(ctx: click.Context, image: str, jobname: str, config: str, with_gui: bool):
    try:
        artefacts_config = read_config(config)
    except FileNotFoundError:
        raise click.ClickException(f"Project config file not found: {config}")
    project = artefacts_config["project"]
    handler = ContainerMgr()
    params = dict(
        image=image,
        project=project,
        jobname=jobname,
        with_gui=with_gui,
        # Hidden settings primarily useful to Artefacts developers
        api_url=os.environ.get("ARTEFACTS_API_URL", DEFAULT_API_URL),
        api_key=os.environ.get("ARTEFACTS_KEY", None),
    )
    container, logs = handler.run(**params)
    if container:
        print(f"Package run complete: Container Id for inspection: {container['Id']}")
    else:
        print("Package run failed:")
        for entry in logs:
            print("\t- " + entry)
