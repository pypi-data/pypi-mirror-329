from rekuest_next.structures.default import (
    get_default_structure_registry,
    id_shrink
)
from rekuest_next.widgets import SearchWidget
from rekuest_next.api.schema import PortScope

from alpaka.api.schema import (
    Room,
    aget_room,
)

structure_reg = get_default_structure_registry()
structure_reg.register_as_structure(
    Room,
    identifier="@alpaka/room",
    scope=PortScope.GLOBAL,
    aexpand=aget_room,
    ashrink=id_shrink,
)