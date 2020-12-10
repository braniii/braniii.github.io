#!/usr/bin/env python

import json
import shutil
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

root_dir = Path(__file__).parent

templates_dir = root_dir / "templates"
styles_dir = root_dir / "styles"
page_data_dir = root_dir / "data"
assets_dir = root_dir / "assets"
build_dir = root_dir / "build"
build_static_dir = build_dir / "static"

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_page(page_name: str):
    template = env.get_template(f"{page_name}.html")

    with (page_data_dir / f"{page_name}.json").open("r") as fp:
        data = json.load(fp)

    with (build_dir / f"{page_name}.html").open("w") as fp:
        fp.write(template.render(**data))


if __name__ == "__main__":
    # Implicitly creates build_dir.
    build_static_dir.mkdir(exist_ok=True, parents=True)

    render_page("index")

    for asset in assets_dir.iterdir():
        shutil.copy(asset, build_static_dir)

    if len(sys.argv) > 1 and sys.argv[1] == "full":
        subprocess.run("cd styles; yarn build", shell=True)
