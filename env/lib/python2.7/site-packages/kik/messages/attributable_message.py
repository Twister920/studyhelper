from kik.messages.message import Message
from kik.messages.attribution import CustomAttribution


class AttributableMessage(Message):
    """
    Parent class for messages that support attribution.
    """
    def __init__(self, attribution=None, **kwargs):
        super(AttributableMessage, self).__init__(**kwargs)
        self.attribution = attribution

    def to_json(self):
        output_json = super(AttributableMessage, self).to_json()
        if self.attribution is not None:
            output_json['attribution'] = self.attribution.to_json()

        return output_json

    @classmethod
    def from_json(cls, json):
        message = super(AttributableMessage, cls).from_json(json)

        if 'attribution' in json:
            message.attribution = CustomAttribution.from_json(json['attribution'])

        return message
