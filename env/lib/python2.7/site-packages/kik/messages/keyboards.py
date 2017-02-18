from kik.messages.responses import response_type_mapping, UnknownResponse
from kik.resource import Resource


class Keyboard(Resource):
    """
    Parent class for all keyboards.
    """
    def __init__(self, type, to=None, hidden=None):
        self.type = type
        self.to = to
        self.hidden = hidden

    @classmethod
    def property_mapping(cls):
        return {
            'to': 'to',
            'type': 'type',
            'hidden': 'hidden',
        }


class SuggestedResponseKeyboard(Keyboard):
    """
    A suggested response keyboard as documented at `<https://dev.kik.com/#/docs/messaging#keyboards>`_.

    :param to: (optional) User who will see this keyboard. If None, the keyboard will be shown to all users who don't
        have another keyboard set.
    :type to: str
    :param hidden: (optional) If True, this keyboard will be hidden until the user chooses to see suggested responses.
    :type hidden: bool
    :param responses: (optional) A list of :class:`SuggestedResponse <kik.message.responses.SuggestedResponse>`.
        Defaults to an empty list.
    :type responses: list[kik.message.responses.SuggestedResponse]
    """
    def __init__(self, to=None, hidden=None, responses=None):
        super(SuggestedResponseKeyboard, self).__init__(type='suggested', to=to, hidden=hidden)
        if responses:
            self.responses = responses
        else:
            self.responses = []

    def to_json(self):
        output_json = super(SuggestedResponseKeyboard, self).to_json()
        output_json['responses'] = [response.to_json() for response in self.responses]
        return output_json

    @classmethod
    def from_json(cls, json):
        keyboard = super(SuggestedResponseKeyboard, cls).from_json(json)

        if 'responses' in json:
            for response in json['responses']:
                response_type = response['type']
                response_cls = response_type_mapping.get(response_type, UnknownResponse)
                if response_cls is not UnknownResponse:
                    del response['type']
                keyboard.responses.append(response_cls.from_json(response))
                response['type'] = response_type

        return keyboard


class UnknownKeyboard(Keyboard):
    """
    This keyboard type is returned by the keyboard factory when it encounters an unknown keyboard type.

    It's `type` attribute is set to the type of the keyboard, and it's `raw_keyboard` attribute contains the raw JSON
    keyboard received
    """
    @classmethod
    def from_json(cls, json):
        keyboard = super(UnknownKeyboard, cls).from_json(json)
        keyboard.raw_keyboard = json
        return keyboard

    @classmethod
    def property_mapping(cls):
        mapping = super(UnknownKeyboard, cls).property_mapping()
        mapping.update({
            'type': 'type'
        })
        return mapping


keyboard_type_mapping = {
    'suggested': SuggestedResponseKeyboard
}


def keyboard_from_json(keyboard):
    kb_type = keyboard['type']
    kb_cls = keyboard_type_mapping.get(kb_type, UnknownKeyboard)
    if kb_cls is not UnknownKeyboard:
        del keyboard['type']
    keyboard_object = kb_cls.from_json(keyboard)
    keyboard['type'] = kb_type
    return keyboard_object
