import pytest
from plottica.lineplot import lineplot
from plottica.set_theme import set_theme
import seaborn as sns


def test_lineplot_wrapper():
    """Test if lineplot is correctly wrapped from seaborn.lineplot"""
    assert callable(lineplot), "lineplot should be callable like seaborn.lineplot."


def test_set_theme_wrapper():
    """Test if set_theme is correctly wrapped from seaborn.set_theme"""
    assert callable(set_theme), "set_theme should be callable like seaborn.set_theme."


def test_lineplot_function():
    """Test if lineplot runs without error"""
    try:
        lineplot(x=[1, 2, 3], y=[4, 5, 6])
    except Exception as e:
        pytest.fail(f"lineplot() raised an exception: {e}")


def test_set_theme_function():
    """Test if set_theme correctly applies Seaborn themes"""
    set_theme(style="darkgrid")

    # Check if Seaborn's theme is applied
    assert sns.axes_style()["axes.grid"], "set_theme() did not apply the expected grid style."
