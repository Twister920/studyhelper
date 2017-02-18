from kik.resource import Resource


class Attribution(Resource):
    """
    Parent class for all attribution types
    """
    pass


class CustomAttribution(Attribution):
    """
    Attribution class for custom attributions, as documented at `<https://dev.kik.com/#/docs/messaging#attribution>`_

    Usage:

    >>> from kik.messages import CustomAttribution, LinkMessage
    >>> message = LinkMessage()
    >>> message.attribution = CustomAttribution(
    >>>     name='A Name',
    >>>     icon_url='http://foo.bar/anicon'
    >>> )
    """
    def __init__(self, name=None, icon_url=None):
        self.name = name
        self.icon_url = icon_url

    @classmethod
    def property_mapping(cls):
        return {
            'name': 'name',
            'icon_url': 'iconUrl'
        }


class PresetAttribution(Attribution):
    """
    Attribution class for the preset attribution types (e.g. "gallery" or "camera")
    """
    def __init__(self, preset_name):
        self.preset_name = preset_name

    def to_json(self):
        return self.preset_name


class PresetAttributions(object):
    """
    List of preset attribution types.

    Valid only on :class:`PictureMessage <kik.messages.PictureMessage>` and
        :class:`VideoMessage <kik.messages.VideoMessage>`.

    :cvar GALLERY: Makes the message appear to be from a user's gallery.
    :vartype GALLERY: kik.message.attribution.PresetAttribution
    :cvar CAMERA: Makes the message appear to be from a camera.
    :vartype CAMERA: kik.message.attribution.PresetAttribution

    Usage:

    >>> from kik.messages import PresetAttributions, PictureMessage
    >>> message = PictureMessage()
    >>> message.attribution = PresetAttributions.CAMERA
    """
    GALLERY = PresetAttribution('gallery')
    CAMERA = PresetAttribution('camera')
