import mirror_requests
import pytest


@pytest.mark.basic
def test_basic_get():
    url = 'https://raw.githubusercontent.com/miurahr/mirror_requests/master/README.rst'
    r = mirror_requests.get(url)
    assert r is not None


@pytest.mark.basic
def test_basic_get_redirect():
    url = 'https://download.qt.io/online/qtsdkrepository/linux_x64/desktop/qt5_53/Updates.xml'
    r = mirror_requests.get(url)
    assert r is not None