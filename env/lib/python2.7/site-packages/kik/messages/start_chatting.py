from kik.messages.message import Message


class StartChattingMessage(Message):
    """
    A full start-chatting message object, as documented at `<https://dev.kik.com/#/docs/messaging#start-chatting>`_.
    """
    def __init__(self, **kwargs):
        super(StartChattingMessage, self).__init__(type='start-chatting', **kwargs)
