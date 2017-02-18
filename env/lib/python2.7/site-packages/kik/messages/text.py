from kik.messages.keyboard_message import KeyboardMessage


class TextMessage(KeyboardMessage):
    """
    A full link message object, as documented at `<https://dev.kik.com/#/docs/messaging#text>`_.
    """
    def __init__(self, to=None, chat_id=None, body=None, keyboards=None, mention=None, delay=None, type_time=None,
                 **kwargs):
        super(TextMessage, self).__init__(type='text', to=to, chat_id=chat_id, mention=mention, delay=delay,
                                          keyboards=keyboards, **kwargs)
        self.body = body
        self.type_time = type_time

    @classmethod
    def property_mapping(cls):
        mapping = super(TextMessage, cls).property_mapping()
        mapping.update({
            'body': 'body',
            'type_time': 'typeTime'
        })
        return mapping
