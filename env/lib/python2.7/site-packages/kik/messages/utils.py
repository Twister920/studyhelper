from kik.messages import TextMessage, LinkMessage, PictureMessage, VideoMessage, StartChattingMessage, \
    ScanDataMessage, StickerMessage, IsTypingMessage, DeliveryReceiptMessage, ReadReceiptMessage, UnknownMessage, \
    FriendPickerMessage

incoming_type_mapping = {
    'text': TextMessage,
    'link': LinkMessage,
    'picture': PictureMessage,
    'video': VideoMessage,
    'start-chatting': StartChattingMessage,
    'scan-data': ScanDataMessage,
    'sticker': StickerMessage,
    'is-typing': IsTypingMessage,
    'delivery-receipt': DeliveryReceiptMessage,
    'read-receipt': ReadReceiptMessage,
    'friend-picker': FriendPickerMessage
}


def messages_from_json(messages):
    """
    Converts incoming JSON format messages into message objects.

    :param messages: A list of messages in JSON format.
    :type messages: list[dict].
    :returns: A list of messages as Python classes.
    :rtype: list[kik.messages.Message].
    """
    message_objects = []
    for message in messages:
        msg_type = message['type']
        msg_cls = incoming_type_mapping.get(msg_type, UnknownMessage)
        if msg_cls is not UnknownMessage:
            # Unknown message types want to keep the type param, as it's not otherwise accessible.
            del message['type']
        message_objects.append(msg_cls.from_json(message))
        message['type'] = msg_type
    return message_objects
