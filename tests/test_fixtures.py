from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat
import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
def test_fixtures(line, title, text, expected):
    print(mdformat.plugins.PARSER_EXTENSIONS)
    output = mdformat.text(text, extensions={"footnote"})
    print(output)
    assert output.rstrip() == expected.rstrip(), output
