import pytest

from text_parser.custom_parsers.listeners.parse import Parse
from text_parser.custom_parsers.listeners.root_listener import RootListener
from tests import SAMPLES_DIR


@pytest.mark.parametrize('sample_name', [
    'test_sample.txt',
])
def test_example(sample_name):
    Parse.parse(SAMPLES_DIR / sample_name, RootListener)
