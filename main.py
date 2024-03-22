import typer
from commands.log import Log
app = typer.Typer()



@app.command()
def create_log(username: str, file_path="C:/", extension='.log'):
    command = Log(username=username, path=file_path, extension=extension)
    command.execute()


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()