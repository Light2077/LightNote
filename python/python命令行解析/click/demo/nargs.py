import click


@click.command()
@click.option('--names', nargs=14, type=str)
def show(names):
    for name in names:
        click.echo("hello %s" % name)

if __name__ == "__main__":
    show()