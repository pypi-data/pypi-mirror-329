from kalpaa import __version__
import kalpaa


def test_version():
	assert kalpaa.get_version() == __version__
