import typer
from commands.log import Log
from typing import Optional
from commands.invoker import CommandInvoker


app = typer.Typer()
typer.Option()

@app.command()
def create_log(username: str = "user", file_path="C:/", extension='.log', balance: Optional[float] = None,
               set_date: str = None,
               title: Optional[str] = None,
               clean: bool = True
               ):
    _user_data = [username, balance, title]
    log_command = Log(path=file_path, extension=extension, user_data=_user_data, clean=clean)
    command_invoker = CommandInvoker()
    command_invoker.set_command(log_command)
    command_invoker.execute_command()


@app.command()
def goodbye():
    print("Goodbye!")


if __name__ == "__main__":
    app()
