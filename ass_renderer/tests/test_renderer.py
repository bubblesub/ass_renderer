from pathlib import Path

import pytest
from ass_parser import read_ass
from PIL import Image, ImageChops

from ass_renderer import AssRenderer

DUMMY_ASS_FILE = """\N{BOM}[Script Info]
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,55,&H00E7F4FF,&H000000FF,&H0025315A,&H00000000,-1,0,0,0,100,100,0,0,1,2.5,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:06.21,0:00:07.22,Default,,0,0,0,,Ako!{NOTE:アコ}
Dialogue: 0,0:00:08.71,0:00:10.95,Default,,0,0,0,,- Shizu!\\N- Ako!
"""

TESTS_PATH = Path(__file__).parent


@pytest.mark.parametrize("pts", [0, 6210, 8710])
def test_ass_renderer(pts: int) -> None:
    ass_file = read_ass(DUMMY_ASS_FILE)

    renderer = AssRenderer()
    renderer.set_source(
        ass_file=ass_file,
        video_resolution=(800, 600),
    )
    output_image = renderer.render(pts).convert("RGBA")

    source_image = Image.open(TESTS_PATH / f"image_{pts}.png").convert("RGBA")

    diff = ImageChops.difference(output_image, source_image)
    assert not diff.getbbox(), "images are different"
