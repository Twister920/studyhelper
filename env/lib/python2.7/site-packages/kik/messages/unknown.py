from kik.messages.message import Message


class UnknownMessage(Message):
    """
    This message type is returned by the message factory when it encounters an unknown message type.

    It's `type` attribute is set to the type of the message, and it's `raw_message` attribute contains the raw JSON
    message received
    """
    @classmethod
    def from_json(cls, json):
        message = super(UnknownMessage, cls).from_json(json)
        message.raw_message = json
        return message

    @classmethod
    def property_mapping(cls):
        mapping = super(UnknownMessage, cls).property_mapping()
        mapping.update({
            'type': 'type'
        })
        return mapping
