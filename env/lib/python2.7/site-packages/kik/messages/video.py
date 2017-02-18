from kik.messages.keyboard_message import KeyboardMessage
from kik.messages.attributable_message import AttributableMessage


class VideoMessage(KeyboardMessage, AttributableMessage):
    """
    A full video message object, as documented at `<https://dev.kik.com/#/docs/messaging#video>`_.
    """
    def __init__(self, to=None, chat_id=None, video_url=None, loop=None, muted=None, autoplay=None, no_save=None,
                 keyboards=None, attribution=None, mention=None, delay=None, **kwargs):
        super(VideoMessage, self).__init__(type='video', to=to, chat_id=chat_id, mention=mention, delay=delay,
                                           keyboards=keyboards, attribution=attribution, **kwargs)
        self.video_url = video_url
        self.loop = loop
        self.muted = muted
        self.autoplay = autoplay
        self.no_save = no_save

    @classmethod
    def property_mapping(cls):
        mapping = super(VideoMessage, cls).property_mapping()
        mapping.update({
            'video_url': 'videoUrl',
            'loop': 'loop',
            'muted': 'muted',
            'autoplay': 'autoplay',
            'no_save': 'noSave'
        })
        return mapping
