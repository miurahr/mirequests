import mirequests
import pytest


@pytest.mark.basic
def test_basic_get():
    url = 'https://raw.githubusercontent.com/miurahr/mirror_requests/master/README.rst'
    r = mirequests.get(url)
    assert r is not None


@pytest.mark.basic
def test_basic_get_redirect():
    url = 'https://download.qt.io/online/qtsdkrepository/linux_x64/desktop/qt5_53/Updates.xml'
    r = mirequests.get(url)
    assert r is not None