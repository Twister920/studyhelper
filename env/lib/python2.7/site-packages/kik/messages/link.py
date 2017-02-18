from kik.messages.keyboard_message import KeyboardMessage
from kik.messages.attributable_message import AttributableMessage


class LinkMessage(KeyboardMessage, AttributableMessage):
    """
    A full link message object, as documented at `<https://dev.kik.com/#/docs/messaging#link>`_.
    """
    def __init__(self, to=None, chat_id=None, url=None, title=None, text=None, pic_url=None, no_forward=None,
                 kik_js_data=None, keyboards=None, attribution=None, mention=None, delay=None, **kwargs):
        super(LinkMessage, self).__init__(type='link', to=to, chat_id=chat_id, mention=mention, delay=delay,
                                          keyboards=keyboards, attribution=attribution, **kwargs)
        self.url = url
        self.title = title
        self.text = text
        self.pic_url = pic_url
        self.no_forward = no_forward
        self.kik_js_data = kik_js_data

    @classmethod
    def property_mapping(cls):
        mapping = super(LinkMessage, cls).property_mapping()
        mapping.update({
            'url': 'url',
            'title': 'title',
            'text': 'text',
            'no_forward': 'noForward',
            'kik_js_data': 'kikJsData',
            'pic_url': 'picUrl'
        })
        return mapping
