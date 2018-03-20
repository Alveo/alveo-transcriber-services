import click

from application import db

@click.group()
def cli():
    pass

@click.command()
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("Database has been rebuilt.")

cli.add_command(init_db)

if __name__ == '__main__':
    cli()

