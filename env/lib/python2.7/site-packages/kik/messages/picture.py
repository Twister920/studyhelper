from kik.messages.keyboard_message import KeyboardMessage
from kik.messages.attributable_message import AttributableMessage


class PictureMessage(KeyboardMessage, AttributableMessage):
    """
    A full picture message object, as documented at `<https://dev.kik.com/#/docs/messaging#picture>`_.
    """
    def __init__(self, to=None, chat_id=None, pic_url=None, keyboards=None, attribution=None, mention=None,
                 delay=None, **kwargs):
        super(PictureMessage, self).__init__(type='picture', to=to, chat_id=chat_id, mention=mention, delay=delay,
                                             keyboards=keyboards, attribution=attribution, **kwargs)
        self.pic_url = pic_url

    @classmethod
    def property_mapping(cls):
        mapping = super(PictureMessage, cls).property_mapping()
        mapping.update({
            'pic_url': 'picUrl'
        })
        return mapping
