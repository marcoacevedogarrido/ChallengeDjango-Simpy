import pytest

def q():
    raise SystemExit(1)

def test_superm():
    with pytest.raises(SystemExit):
        q()
