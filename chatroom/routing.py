# -*- coding: utf-8 -*-
from channels.routing import route
from channels import include
from .consumers import (
    chat_connection, chat_receive, chat_disconnect, loadhistory_connect,
    loadhistory_disconnect, loadhistory_receive
)

chat_routing = [
    route("websocket.connect", chat_connection),
    route("websocket.receive", chat_receive),
    route("websocket.disconnect", chat_disconnect)
]

loadhistory_routing = [
    route("websocket.connect", loadhistory_connect),
    route("websocket.receive", loadhistory_receive),
    route("websocket.disconnect", loadhistory_disconnect)
]

channel_routing = [
    include(chat_routing, path=r"^/chat/$"),
    include(loadhistory_routing, path=r"^/loadhistory/$"),
]
