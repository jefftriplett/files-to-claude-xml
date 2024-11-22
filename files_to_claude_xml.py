# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
#     "typer",
#     "python-docx",
#     "pdfminer.six",
# ]
# ///
import mimetypes
from pathlib import Path
from typing import Annotated, Iterator

import typer
from rich import print


def read_docx_content(file_path: Path) -> str:
    from docx import Document
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

__version__ = "2024.11.22"


app = typer.Typer()



def read_text_file(file_path: Path) -> str:
    return file_path.read_text()


def read_pdf_content(file_path: Path) -> str:
    from io import StringIO
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams

    output_string = StringIO()
    with open(file_path, 'rb') as fin:
        extract_text_to_fp(fin, output_string, laparams=LAParams())
    return output_string.getvalue().strip()


def read_file_content(file_path: Path) -> str:
    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        match mime_type:
            case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return read_docx_content(file_path)
            case 'application/pdf':
                return read_pdf_content(file_path)
            case 'text/plain':
                return read_text_file(file_path)
            case _:
                return read_text_file(file_path)
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {str(e)}")


def gather_files(paths: list[Path], verbose: bool = False) -> Iterator[Path]:
    """
    Recursively gather all files from the given paths.
    If a path is a file, yield it directly.
    If a path is a directory, recursively yield all files within it.
    """
    for path in paths:
        if verbose:
            print(f"Processing path: {path.as_posix()}")

        if path.is_file():
            yield path
        elif path.is_dir():
            if verbose:
                print(f"Scanning directory: {path.as_posix()}")
            # Recursively process all files in the directory
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    if verbose:
                        print(f"Found file: {file_path.as_posix()}")
                    yield file_path


def compile_xml(*, paths: list[Path], verbose: bool = False) -> str:
    xml_parts = ["<documents>"]

    for index, file in enumerate(gather_files(paths, verbose=verbose), start=1):
        if verbose:
            print(f"Processing: {file.as_posix()}")

        try:
            content = read_file_content(file)
            xml_parts.append(f'<document index="{index}">')
            xml_parts.append(f"<source>{file.as_posix()}</source>")
            xml_parts.append("<document_content>")
            xml_parts.append(content)
            xml_parts.append("</document_content>")
            xml_parts.append("</document>")
            if verbose:
                print(f"Successfully processed: {file.as_posix()}")
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
    paths: list[Path] = typer.Argument(..., help="Input files or directories to process"),
    output: Path = typer.Option(Path("_claude.xml"), help="Output XML file path"),
    verbose: bool = False,
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback)
    ] = None,
):
    if not paths:
        print("No input paths provided. Please specify at least one file or directory.")
        raise typer.Exit(code=1)

    xml_content = compile_xml(paths=paths, verbose=verbose)

    output.write_text(xml_content)

    if verbose:
        print(f"XML file has been created: {output}")


if __name__ == "__main__":
    app()
