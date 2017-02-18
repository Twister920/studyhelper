from kik.resource import Resource


class SuggestedResponse(Resource):
    """
    Base class for all responses for :class:`SuggestedResponseKeyboard<kik.messages.SuggestedResponseKeyboard>`.
    """
    def __init__(self, type):
        self.type = type

    @classmethod
    def property_mapping(cls):
        return {'type': 'type'}


class TextResponse(SuggestedResponse):
    """
    A text response, as documented at `<https://dev.kik.com/#/docs/messaging#suggested-response-keyboard>`_.
    """
    def __init__(self, body):
        super(TextResponse, self).__init__(type='text')
        self.body = body

    @classmethod
    def property_mapping(cls):
        mapping = super(TextResponse, cls).property_mapping()
        mapping.update({'body': 'body'})
        return mapping


class FriendPickerResponse(SuggestedResponse):
    """
    A friend picker response as documented on https://dev.kik.com/#/docs/messaging#friend-picker-response-object
    """
    def __init__(self, body=None, min=None, max=None, preselected=None):
        super(FriendPickerResponse, self).__init__(type='friend-picker')
        self.body = body
        self.min = min
        self.max = max
        self.preselected = preselected

    @classmethod
    def property_mapping(cls):
        mapping = super(FriendPickerResponse, cls).property_mapping()

        mapping.update({
            'body': 'body',
            'min': 'min',
            'max': 'max',
            'preselected': 'preselected'
        })

        return mapping


class UnknownResponse(SuggestedResponse):
    """
    This response type is returned by the response factory when it encounters an unknown response type.

    It's `type` attribute is set to the type of the response, and it's `raw_response` attribute contains the raw JSON
    response received
    """
    @classmethod
    def from_json(cls, json):
        response = super(UnknownResponse, cls).from_json(json)
        response.raw_response = json
        return response

    @classmethod
    def property_mapping(cls):
        mapping = super(UnknownResponse, cls).property_mapping()
        mapping.update({
            'type': 'type'
        })
        return mapping


response_type_mapping = {
    'text': TextResponse,
    'friend-picker': FriendPickerResponse
}
