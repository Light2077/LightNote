import click


@click.command()
@click.option('--name', type=str)
@click.option('--age', type=int)
def show(name, age):
    print("I'm %s, %s years old." % (name, age))

if __name__ == "__main__":
    show()