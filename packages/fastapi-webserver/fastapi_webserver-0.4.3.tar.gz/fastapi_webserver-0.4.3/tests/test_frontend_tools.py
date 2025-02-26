import tempfile
import unittest
from pathlib import Path

RESOURCES_FOLDER: Path = Path(__file__).parent / "resources"
TEMP_FOLDER: Path = Path(tempfile.gettempdir())


class TestFrontendTools(unittest.TestCase):
    def test_sass_compiler(self):
        from webserver.frontend import css

        output: Path = TEMP_FOLDER / "styles.css"
        map: Path = TEMP_FOLDER / "styles.css.map"

        css.compile(source=(RESOURCES_FOLDER / "assets/sass/theme.scss"), output=output)

        assert output.exists() and map.exists()
        assert output.read_text(encoding="utf-8") == "html{color:#000 !important}/*# sourceMappingURL=styles.css.map */\n"
