import matplotlib.pyplot as _plt

class PyplotWrapper:
    def __getattr__(self, name):
        return getattr(_plt, name)

pyplot = PyplotWrapper()