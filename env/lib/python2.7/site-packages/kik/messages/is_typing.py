from kik.messages.message import Message


class IsTypingMessage(Message):
    """
    A full is-typing message object, as documented at `<https://dev.kik.com/#/docs/messaging#is-typing>`_.
    """
    def __init__(self, is_typing=None, **kwargs):
        super(IsTypingMessage, self).__init__(type='is-typing', **kwargs)
        self.is_typing = is_typing

    @classmethod
    def property_mapping(cls):
        mapping = super(IsTypingMessage, cls).property_mapping()
        mapping.update({
            'is_typing': 'isTyping'
        })
        return mapping
