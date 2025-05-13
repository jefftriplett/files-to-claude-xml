# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
#     "typer",
# ]
# ///

from pathlib import Path
from typing import Annotated

import typer
from rich import print

__version__ = "2024.10.4"


app = typer.Typer()


def compile_xml(*, files: list[Path], verbose: bool = False) -> str:
    xml_parts = ["<documents>"]
    index = 1

    for file in files:
        if verbose:
            print(file.as_posix())

        try:
            content = file.read_text()
            xml_parts.append(f'<document index="{index}">')
            xml_parts.append(f"<source>{file.as_posix()}</source>")
            xml_parts.append("<document_content>")
            xml_parts.append(content)
            xml_parts.append("</document_content>")
            xml_parts.append("</document>")
            index += 1

        except Exception as e:
            print(f"[red]Error reading file: {str(e)}[/red]")

    xml_parts.append("</documents>")

    return "\n".join(xml_parts)


def version_callback(value: bool):
    if value:
        print(f"files-to-claude-xml version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    files: list[Path] = typer.Argument(..., help="Input files to process"),
    output: Path = typer.Option(Path("_claude.xml"), help="Output XML file path"),
    verbose: bool = False,
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback)
    ] = None,
):
    if not files:
        print("No input files provided. Please specify at least one file.")
        raise typer.Exit(code=1)

    xml_content = compile_xml(files=files, verbose=verbose)

    output.write_text(xml_content)

    if verbose:
        print(f"XML file has been created: {output}")


if __name__ == "__main__":
    app()
