from .vars import get_current_alpaka
from koil import unkoil
from alpaka.rath import AlpakaRath, current_alpaka_rath


def execute(operation, variables, rath: AlpakaRath = None):
    rath = rath or current_alpaka_rath.get()
    return operation(
        **rath.query(
            operation.Meta.document,
            operation.Arguments(**variables).dict(by_alias=True),
        ).data
    )


async def aexecute(operation, variables, rath: AlpakaRath = None):
    rath = rath or current_alpaka_rath.get()

    x = await rath.aquery(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    )
    return operation(**x.data)


def subscribe(operation, variables, rath: AlpakaRath = None):
    rath = rath or current_alpaka_rath.get()

    for ev in rath.subscribe(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    ):
        yield operation(**ev.data)


async def asubscribe(operation, variables, rath: AlpakaRath = None):
    rath = rath or current_alpaka_rath.get()
    async for event in rath.asubscribe(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    ):
        yield operation(**event.data)


async def achat(*args, **kwargs):
    alpaka = get_current_alpaka()
    return await alpaka.chat(*args, **kwargs)


def chat(*args, **kwargs):
    return unkoil(achat, *args, **kwargs)


async def apull(*args, **kwargs):
    alpaka = get_current_alpaka()
    print(args, kwargs)
    return await alpaka.pull(*args, **kwargs)


def pull(*args, **kwargs):
    return unkoil(apull, *args, **kwargs)
