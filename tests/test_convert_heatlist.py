import os
import csv
import sys
import types
import pytest

def _stub_external_modules():
    requests = types.ModuleType('requests')
    adapters = types.ModuleType('requests.adapters')
    class HTTPAdapter:
        def __init__(self, *args, **kwargs):
            pass
    adapters.HTTPAdapter = HTTPAdapter
    class Session:
        def mount(self, *args, **kwargs):
            pass
        def get(self, *args, **kwargs):
            class Response:
                status_code = 200
                content = b''
            return Response()
    requests.Session = Session
    requests.adapters = adapters
    requests.exceptions = types.SimpleNamespace(RequestException=Exception)
    requests.__path__ = []
    sys.modules['requests'] = requests
    sys.modules['requests.adapters'] = adapters

    urllib3 = types.ModuleType('urllib3')
    util = types.ModuleType('urllib3.util')
    retry = types.ModuleType('urllib3.util.retry')
    class Retry:
        def __init__(self, *args, **kwargs):
            pass
    retry.Retry = Retry
    util.retry = retry
    urllib3.util = util
    sys.modules['urllib3'] = urllib3
    sys.modules['urllib3.util'] = util
    sys.modules['urllib3.util.retry'] = retry


def _write_csv(rows):
    os.makedirs('log', exist_ok=True)
    with open('log/heat_list.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


@pytest.fixture(autouse=True)
def stub_modules():
    _stub_external_modules()
    yield
    for m in [
        'requests',
        'requests.adapters',
        'urllib3',
        'urllib3.util',
        'urllib3.util.retry',
    ]:
        sys.modules.pop(m, None)


def test_load_heat_list_reads_all_heats():
    rows = [
        ['e', 'pilot1', 'x', '1'],
        ['e', 'pilot2', 'y', '2'],
        ['e', 'pilot3', 'z', '3'],
    ]
    _write_csv(rows)
    from src.droras.convert_heatlist import load_heat_list
    heatlist = load_heat_list()
    assert ['pilot3', 3, 'z'] in heatlist


def test_get_heat_pilots_returns_csv():
    rows = [
        ['e', 'p1', 'x', '1'],
        ['e', 'p2', 'y', '2'],
    ]
    _write_csv(rows)
    from src.droras.convert_heatlist import load_heat_list, get_heat_pilots
    heatlist = load_heat_list()
    assert get_heat_pilots(1, heatlist) == 'p1,1,x'

