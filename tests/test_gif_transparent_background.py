from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

SOURCE = "course/images/sticker.gif"


def test_resized_gif_keeps_transparent_background():
    with open(SOURCE, "rb") as f:
        buffer = f.read()

    config = Config()
    config.PILLOW_PRESERVE_INDEXED_MODE = True
    engine = Engine(Context(config=config))
    engine.load(buffer, ".gif")
    engine.resize(240, 160)
    out = engine.read(".gif")

    img = Image.open(BytesIO(out)).convert("RGBA")
    assert img.size == (240, 160)
    # The top-left corner is transparent in the source sticker.
    assert img.getpixel((0, 0))[3] == 0
