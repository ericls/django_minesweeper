from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group


def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


def ws_add(message):
    path = message.content["path"][1: -1]
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group(path).add(message.reply_channel)


def ws_message(message):
    path = message.content["path"][1: -1]
    Group(path).send({
        # "text": "[Hello] this is game: %s" % path,
        "text": message.content["text"],
    })


def ws_disconnect(message):
    path = message.content["path"][1: -1]
    Group(path).discard(message.reply_channel)
