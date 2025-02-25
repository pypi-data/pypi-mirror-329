import anyio
from anyio.streams.memory import MemoryObjectReceiveStream
import mcp.types as types


class InterceptingStream(MemoryObjectReceiveStream[types.JSONRPCMessage | Exception]):
    def __init__(self, original_stream: MemoryObjectReceiveStream[types.JSONRPCMessage | Exception]):
        # We don't call super().__init__() with a queue; we store the original stream.
        self._original_stream = original_stream

    async def receive(self) -> types.JSONRPCMessage | Exception:
        """
        Intercepts the next incoming JSONRPCMessage (or Exception), rewrites it if necessary,
        then returns it for normal MCP handling.
        """
        message = await self._original_stream.receive()

        # Only intercept if it's a JSONRPCMessage (not an Exception).
        if isinstance(message, types.JSONRPCMessage):
            # Check if it's something like { "method": "notifications/cancelled", ... }
            if getattr(message.root, "method", None) == "notifications/cancelled":
                # Rewrite into a recognized "progress" message, with negative progress
                # as your custom "cancel" signal.
                new_params = {
                    "progressToken": message.root.params.get("requestId", ""),
                    "progress": -1.0,
                    "total": None
                }
                message.root.method = "notifications/progress"
                message.root.params = new_params

        return message

    async def aclose(self) -> None:
        """
        Ensure we close the underlying stream when we're done.
        """
        await self._original_stream.aclose()

    def clone(self) -> "InterceptingStream":
        """
        If MCP or any libraries call clone(), we can provide a cloned InterceptingStream.
        """
        return InterceptingStream(self._original_stream.clone())
