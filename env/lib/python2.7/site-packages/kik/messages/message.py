from kik.resource import Resource


class Message(Resource):
    """
    Parent class for all messages.
    """
    def __init__(self, type, to=None, id=None, chat_id=None, mention=None, participants=None, from_user=None,
                 delay=None, read_receipt_requested=None, timestamp=None):
        self.type = type
        self.to = to
        self.id = id
        self.chat_id = chat_id
        self.mention = mention
        self.participants = participants
        self.from_user = from_user
        self.delay = delay
        self.read_receipt_requested = read_receipt_requested
        self.timestamp = timestamp

    @classmethod
    def property_mapping(cls):
        return {
            'type': 'type',
            'id': 'id',
            'chat_id': 'chatId',
            'mention': 'mention',
            'participants': 'participants',
            'to': 'to',
            'from_user': 'from',
            'delay': 'delay',
            'read_receipt_requested': 'readReceiptRequested',
            'timestamp': 'timestamp'
        }
