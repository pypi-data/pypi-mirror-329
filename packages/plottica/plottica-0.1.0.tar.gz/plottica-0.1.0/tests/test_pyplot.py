from plottica import pyplot

def test_pyplot():
    assert hasattr(pyplot, "plot")
    assert hasattr(pyplot, "show")