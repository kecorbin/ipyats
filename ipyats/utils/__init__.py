import inspect


def show_source(callable):
    print(inspect.getsource(callable))
