from __future__ import annotations

import collections.abc
import typing

from momotor.rpc.proto.tool_pb2 import ToolSet as ToolSetMessage

TN = typing.TypeVar('TN')


if typing.TYPE_CHECKING:
    from momotor.options.tools.types import ToolSet as ToolSetType


def toolsets_to_message(toolsets: collections.abc.Iterable["ToolSetType"]) -> collections.abc.Iterable[ToolSetMessage]:
    """ Convert an iterable of ToolName objects into a sequence of Tool messages
    """
    for toolset in toolsets:
        yield ToolSetMessage(
            tool=[str(tool) for tool in toolset]
        )


def message_to_toolsets(toolset_message: collections.abc.Sequence[ToolSetMessage] | None) \
        -> collections.abc.Iterable[frozenset[str]]:
    """ Convert a sequence of Tool messages back into an iterable of tool sets """
    if toolset_message:
        for msg in toolset_message:
            yield frozenset(msg.tool)
