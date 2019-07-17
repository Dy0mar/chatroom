# -*- coding: utf-8 -*-
import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from channels_presence.decorators import touch_presence
from channels_presence.models import Room
from channels_presence.signals import presence_changed
from django.dispatch import receiver
from django.utils.html import escape

from .models import ChatMessage


@channel_session_user_from_http
def chat_connection(message):
    Group("all").add(message.reply_channel)
    Room.objects.add("all", message.reply_channel.name, message.user)
    message.reply_channel.send({"accept": True})


@touch_presence
@channel_session_user
def chat_receive(message):
    data = json.loads(message['text'])

    if not data['message']:
        return
    if not message.user.is_authenticated:
        return

    current_message = escape(data['message'])
    m = ChatMessage(
        user=message.user,
        message=data['message'],
        message_html=escape(data['message'])
    )
    m.save()
    context = {'user': m.user.username, 'message': current_message}
    Group("all").send({'text': json.dumps(context)})


@channel_session_user
def chat_disconnect(message):
    Group("all").discard(message.reply_channel)
    Room.objects.remove("all", message.reply_channel.name)


@receiver(presence_changed)
def broadcast_presence(sender, room, **kwargs):
    # Broadcast the new list of present users to the room.
    Group(room.channel_name).send({
        'text': json.dumps({
            'type': 'presence',
            'payload': {
                'channel_name': room.channel_name,
                'members': [user.username for user in room.get_users()],
                'lookers': int(room.get_anonymous_count()),
            }
        })
    })


@channel_session_user_from_http
def loadhistory_connect(message):
    message.reply_channel.send({"accept": True})


@channel_session_user
def loadhistory_disconnect(message):
    pass


@channel_session_user
def loadhistory_receive(message):
    data = json.loads(message['text'])

    queryset = ChatMessage.objects.filter(
        id__lte=data['last_message_id']
    ).order_by("-created")[:10]

    count_messages = len(queryset)

    previous_message_id = -1
    if count_messages > 0:
        last_message_id = queryset[count_messages - 1].id
        previous_message = ChatMessage.objects.filter(
            pk__lt=last_message_id
        ).order_by("-pk").first()
        if previous_message:
            previous_message_id = previous_message.id

    chat_messages = reversed(queryset)
    cleaned_chat_messages = list()
    for item in chat_messages:
        current_message = item.message_html
        cleaned_item = {'user': item.user.username, 'message': current_message}
        cleaned_chat_messages.append(cleaned_item)

    my_dict = {
        'messages': cleaned_chat_messages,
        'previous_id': previous_message_id
    }
    message.reply_channel.send({'text': json.dumps(my_dict)})
