from kik.resource import Resource

HOSTED_URL = 'https://api.kik.com/v1/code/{id}{color_query}'


class Code(Resource):
    """
    Model representing a Kik Code. Can be instantiated with a Kik Code ID, or created using
    :func:`kik.KikApi.create_code`.

    :ivar id: The ID for the Kik Code.
    :vartype id: str
    """
    class Colors(object):
        """
        Kik Code color mapping, taken from `<https://dev.kik.com/#/docs/messaging#kik-code-colors>`_
        """
        KIK_BLUE = 0
        TURQUOISE = 1
        MINT = 2
        FOREST = 3
        KIK_GREEN = 4
        SUNSHINE = 5
        ORANGE_CREAMSICLE = 6
        BLOOD_ORANGE = 7
        CANDY_APPLE_RED = 8
        SALMON = 9
        CORAL = 10
        CRANBERRY = 11
        LAVENDER = 12
        ROYAL_PURPLE = 13
        MARINE = 14
        STEEL = 15

    def __init__(self, id, **kwargs):
        super(Code, self).__init__()
        self.id = id

    def url(self, color=None):
        """
        Returns the URL for the Kik Code.

        :param color: (optional) Sets the color of the Kik Code. For options see :class:`kik.Code.Colors`
        :type color: int
        """
        color_query = '?c={}'.format(color) if color else ''
        return HOSTED_URL.format(id=self.id, color_query=color_query)

    @classmethod
    def property_mapping(cls):
        mapping = {
            'id': 'id',
        }
        return mapping
