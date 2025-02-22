from .alpaka import Alpaka
from .funcs import chat, achat

try:
    from .arkitekt import ArkitektNextAlpaka
    from .rekuest import structure_reg
except ImportError:
    pass
