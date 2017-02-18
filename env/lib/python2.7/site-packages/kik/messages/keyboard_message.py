from kik.messages.keyboards import keyboard_from_json
from kik.messages.message import Message


class KeyboardMessage(Message):
    """
    Parent class for messages that support keyboards.
    """
    def __init__(self, keyboards=None, **kwargs):
        super(KeyboardMessage, self).__init__(**kwargs)
        if keyboards:
            self.keyboards = keyboards
        else:
            self.keyboards = []

    def to_json(self):
        output_json = super(KeyboardMessage, self).to_json()
        if len(self.keyboards) > 0:
            output_json['keyboards'] = [keyboard.to_json() for keyboard in self.keyboards]

        return output_json

    @classmethod
    def from_json(cls, json):
        message = super(KeyboardMessage, cls).from_json(json)

        if 'keyboards' in json:
            keyboards = []
            for keyboard in json['keyboards']:
                keyboards.append(keyboard_from_json(keyboard))

            if len(keyboards) > 0:
                message.keyboards = keyboards

        return message
