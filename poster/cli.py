from typing import List

import typer

app = typer.Typer()


@app.command()
def rerun():
    typer.echo("Rerun the analysis")


@app.command()
def resume(path: str):
    typer.echo(f"Continue the analysis from {path}")


@app.command()
def run(args: List[str]):
    typer.echo(f"Run a job {args}")


if __name__ == "__main__":
    app()
