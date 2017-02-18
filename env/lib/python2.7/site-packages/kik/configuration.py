from kik.messages.keyboards import keyboard_from_json
from kik.resource import Resource


class Configuration(Resource):
    """
    Model for your bot's configuration.

    :param webhook: URL the API will send incoming messages to
    :type webhook: str
    :param features: Feature flags to set
    :type features: dict
    :param static_keyboard: The static keyboard to set
    :type static_keyboard: kik.messages.keyboards.Keyboard
    """
    def __init__(self, webhook, features=None, static_keyboard=None):
        self.webhook = webhook
        if features is None:
            features = {}
        self.features = features
        self.static_keyboard = static_keyboard

    def to_json(self):
        output_json = super(Configuration, self).to_json()

        if self.static_keyboard:
            output_json['staticKeyboard'] = self.static_keyboard.to_json()

        return output_json

    @classmethod
    def property_mapping(cls):
        return {
            'webhook': 'webhook',
            'features': 'features',
            'static_keyboard': 'staticKeyboard'
        }

    @classmethod
    def from_json(cls, json):
        config = super(Configuration, cls).from_json(json)

        if 'staticKeyboard' in json and json['staticKeyboard']:
            config.static_keyboard = keyboard_from_json(json['staticKeyboard'])
        else:
            config.static_keyboard = None

        return config
