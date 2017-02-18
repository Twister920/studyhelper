from kik.messages.keyboard_message import Message


class FriendPickerMessage(Message):
    """
    A friend picker message, as documented at `<https://dev.kik.com/#/docs/messaging#friend-picker-response-object>`_.
    """
    def __init__(self, picked=None, **kwargs):
        super(FriendPickerMessage, self).__init__(type='friend-picker', **kwargs)
        self.picked = picked

    @classmethod
    def property_mapping(cls):
        mapping = super(FriendPickerMessage, cls).property_mapping()
        mapping.update({
            'picked': 'picked'
        })
        return mapping
