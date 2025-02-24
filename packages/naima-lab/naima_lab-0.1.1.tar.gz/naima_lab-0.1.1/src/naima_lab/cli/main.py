import typer
from naima_lab.cli.main_nlp import app as app_nlp

app = typer.Typer()

app.add_typer(app_nlp, name="nlp")