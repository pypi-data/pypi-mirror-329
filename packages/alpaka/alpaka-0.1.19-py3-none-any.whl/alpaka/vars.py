from contextvars import ContextVar


current_alpaka = ContextVar("current_alpaka", default=None)


def get_current_alpaka():
    return current_alpaka.get()


def set_current_alpaka(value):
    current_alpaka.set(value)
