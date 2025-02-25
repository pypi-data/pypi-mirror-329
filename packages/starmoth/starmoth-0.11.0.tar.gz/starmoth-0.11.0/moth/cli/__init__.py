import click
import numpy as np

from moth import Moth
from moth.server import Server
from moth.message import HandshakeMsg, ImagePromptMsg, ClassificationResultMsg
from moth.driver import NoOpDriver, TestImagesInFolder


def print_askii_image(img):
    size = img.size
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            pixel = np.mean(img.getpixel((x, y)))
            if pixel > 128:
                line += "░"
            else:
                line += " "
        print(line)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--port", default=7171, help="What port the server should bind to")
def server(port):
    """
    Star a moth server

    Provide a path to a folder that contains images. These images will be sent to any
    model that connects.
    """
    server = Server(port)

    @server.driver_factory
    def create_driver_for(handshake: HandshakeMsg):
        print(f"{handshake.name} just connected")
        return NoOpDriver()

    server.start()


@cli.command(help="Start a moth client")
@click.option("--port", default=7171, help="What port to connect to")
@click.option("--host", default="localhost", help="Where is the server running")
@click.option("--name", default="cli-client", help="The name of this client")
def client(port, host, name):
    click.echo("Start a moth client")
    moth = Moth(name, "t123")

    @moth.prompt
    def on_prompt(prompt: ImagePromptMsg) -> ClassificationResultMsg:
        if max(prompt.image.size) < 30:
            print_askii_image(prompt.image)
        else:
            prompt.image.show()
        answer = input("What class? > ")

        return ClassificationResultMsg(prompt_id=prompt.id, class_name=answer)

    server_url = f"tcp://{host}:{port}"
    moth.run(url=server_url)


if __name__ == "__main__":
    cli()
