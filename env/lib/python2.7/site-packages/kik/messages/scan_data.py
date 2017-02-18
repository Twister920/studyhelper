from kik.messages.message import Message


class ScanDataMessage(Message):
    """
    A full scan-data message object, as documented at `<https://dev.kik.com/#/docs/messaging#scan-data>`_.
    """
    def __init__(self, data=None, **kwargs):
        super(ScanDataMessage, self).__init__(type='scan-data', **kwargs)
        self.data = data

    @classmethod
    def property_mapping(cls):
        mapping = super(ScanDataMessage, cls).property_mapping()
        mapping.update({
            'data': 'data'
        })
        return mapping
