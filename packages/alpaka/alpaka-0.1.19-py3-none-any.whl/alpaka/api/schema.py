from typing import Literal, List, Optional, AsyncIterator, Iterator
from alpaka.funcs import subscribe, aexecute, execute, asubscribe
from pydantic import Field, BaseModel, ConfigDict
from rath.scalars import ID
from alpaka.rath import AlpakaRath
from enum import Enum


class StructureInput(BaseModel):
    object: ID
    identifier: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MessageAgentRoom(BaseModel):
    """Room(id, title, description, creator)"""

    typename: Literal["Room"] = Field(alias="__typename", default="Room", exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)


class MessageAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Literal["Agent"] = Field(
        alias="__typename", default="Agent", exclude=True
    )
    id: ID
    room: MessageAgentRoom
    model_config = ConfigDict(frozen=True)


class Message(BaseModel):
    """Message represent the message of an agent on a room"""

    typename: Literal["Message"] = Field(
        alias="__typename", default="Message", exclude=True
    )
    id: ID
    text: str
    "A clear text representation of the rich comment"
    agent: MessageAgent
    "The user that created this comment"
    model_config = ConfigDict(frozen=True)


class ListMessageAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Literal["Agent"] = Field(
        alias="__typename", default="Agent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ListMessage(BaseModel):
    """Message represent the message of an agent on a room"""

    typename: Literal["Message"] = Field(
        alias="__typename", default="Message", exclude=True
    )
    id: ID
    text: str
    "A clear text representation of the rich comment"
    agent: ListMessageAgent
    "The user that created this comment"
    model_config = ConfigDict(frozen=True)


class Room(BaseModel):
    """Room(id, title, description, creator)"""

    typename: Literal["Room"] = Field(alias="__typename", default="Room", exclude=True)
    id: ID
    title: str
    "The Title of the Room"
    description: str
    model_config = ConfigDict(frozen=True)


class SendMutation(BaseModel):
    send: Message

    class Arguments(BaseModel):
        text: str
        room: ID
        agent_id: str = Field(alias="agentId")
        attach_structures: Optional[List[StructureInput]] = Field(
            alias="attachStructures", default=None
        )

    class Meta:
        document = "fragment Message on Message {\n  id\n  text\n  agent {\n    id\n    room {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation Send($text: String!, $room: ID!, $agentId: String!, $attachStructures: [StructureInput!]) {\n  send(\n    input: {text: $text, room: $room, agentId: $agentId, attachStructures: $attachStructures}\n  ) {\n    ...Message\n    __typename\n  }\n}"


class CreateRoomMutation(BaseModel):
    create_room: Room = Field(alias="createRoom")

    class Arguments(BaseModel):
        title: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n  __typename\n}\n\nmutation CreateRoom($title: String, $description: String) {\n  createRoom(input: {title: $title, description: $description}) {\n    ...Room\n    __typename\n  }\n}"


class GetRoomQuery(BaseModel):
    room: Room

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n  __typename\n}\n\nquery GetRoom($id: ID!) {\n  room(id: $id) {\n    ...Room\n    __typename\n  }\n}"


class WatchRoomSubscriptionRoom(BaseModel):
    typename: Literal["RoomEvent"] = Field(
        alias="__typename", default="RoomEvent", exclude=True
    )
    message: Optional[ListMessage] = Field(default=None)
    model_config = ConfigDict(frozen=True)


class WatchRoomSubscription(BaseModel):
    room: WatchRoomSubscriptionRoom

    class Arguments(BaseModel):
        room: ID
        agent_id: ID = Field(alias="agentId")

    class Meta:
        document = "fragment ListMessage on Message {\n  id\n  text\n  agent {\n    id\n    __typename\n  }\n  __typename\n}\n\nsubscription WatchRoom($room: ID!, $agentId: ID!) {\n  room(room: $room, agentId: $agentId) {\n    message {\n      ...ListMessage\n      __typename\n    }\n    __typename\n  }\n}"


async def asend(
    text: str,
    room: ID,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[AlpakaRath] = None,
) -> Message:
    """Send


    Arguments:
        text (str): No description
        room (ID): No description
        agent_id (str): No description
        attach_structures (Optional[List[StructureInput]], optional): No description.
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Message"""
    return (
        await aexecute(
            SendMutation,
            {
                "text": text,
                "room": room,
                "agentId": agent_id,
                "attachStructures": attach_structures,
            },
            rath=rath,
        )
    ).send


def send(
    text: str,
    room: ID,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[AlpakaRath] = None,
) -> Message:
    """Send


    Arguments:
        text (str): No description
        room (ID): No description
        agent_id (str): No description
        attach_structures (Optional[List[StructureInput]], optional): No description.
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Message"""
    return execute(
        SendMutation,
        {
            "text": text,
            "room": room,
            "agentId": agent_id,
            "attachStructures": attach_structures,
        },
        rath=rath,
    ).send


async def acreate_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[AlpakaRath] = None,
) -> Room:
    """CreateRoom


    Arguments:
        title (Optional[str], optional): No description.
        description (Optional[str], optional): No description.
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return (
        await aexecute(
            CreateRoomMutation, {"title": title, "description": description}, rath=rath
        )
    ).create_room


def create_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[AlpakaRath] = None,
) -> Room:
    """CreateRoom


    Arguments:
        title (Optional[str], optional): No description.
        description (Optional[str], optional): No description.
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return execute(
        CreateRoomMutation, {"title": title, "description": description}, rath=rath
    ).create_room


async def aget_room(id: ID, rath: Optional[AlpakaRath] = None) -> Room:
    """GetRoom


    Arguments:
        id (ID): No description
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return (await aexecute(GetRoomQuery, {"id": id}, rath=rath)).room


def get_room(id: ID, rath: Optional[AlpakaRath] = None) -> Room:
    """GetRoom


    Arguments:
        id (ID): No description
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return execute(GetRoomQuery, {"id": id}, rath=rath).room


async def awatch_room(
    room: ID, agent_id: ID, rath: Optional[AlpakaRath] = None
) -> AsyncIterator[WatchRoomSubscriptionRoom]:
    """WatchRoom


    Arguments:
        room (ID): No description
        agent_id (ID): No description
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        WatchRoomSubscriptionRoom"""
    async for event in asubscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room


def watch_room(
    room: ID, agent_id: ID, rath: Optional[AlpakaRath] = None
) -> Iterator[WatchRoomSubscriptionRoom]:
    """WatchRoom


    Arguments:
        room (ID): No description
        agent_id (ID): No description
        rath (alpaka.rath.AlpakaRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        WatchRoomSubscriptionRoom"""
    for event in subscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room
