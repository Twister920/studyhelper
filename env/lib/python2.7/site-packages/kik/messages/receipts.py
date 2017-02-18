from kik.messages.message import Message


class ReceiptMessage(Message):
    """
    Parent class for all receipts.
    """
    def __init__(self, message_ids=None, **kwargs):
        super(ReceiptMessage, self).__init__(**kwargs)
        self.message_ids = message_ids

    @classmethod
    def property_mapping(cls):
        mapping = super(ReceiptMessage, cls).property_mapping()
        mapping.update({
            'message_ids': 'messageIds'
        })
        return mapping


class ReadReceiptMessage(ReceiptMessage):
    """
    A full read-receipt message object, as documented at `<https://dev.kik.com/#/docs/messaging#receipts>`_.
    """
    def __init__(self, **kwargs):
        super(ReadReceiptMessage, self).__init__(type='read-receipt', **kwargs)


class DeliveryReceiptMessage(ReceiptMessage):
    """
    A full delivery-receipt message object, as documented at `<https://dev.kik.com/#/docs/messaging#receipts>`_.
    """
    def __init__(self, **kwargs):
        super(DeliveryReceiptMessage, self).__init__(type='delivery-receipt', **kwargs)
