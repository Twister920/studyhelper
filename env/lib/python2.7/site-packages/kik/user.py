from kik.resource import Resource


class User(Resource):
    """
    Model representing a Kik user's profie information. Created using :func:`kik.KikApi.get_user`.

    :ivar first_name: The user's first name
    :vartype first_name: str
    :ivar last_name: The user's last name
    :vartype last_name: str
    :ivar profile_pic_url: URL for the users's profile picture
    :vartype profile_pic_url: str
    :ivar profile_pic_last_modified: Timestamp indicating when the user's profile picture was
        last modified, to allow for caching
    :vartype: profile_last_modified: int
    """
    def __init__(self, first_name, last_name, profile_pic_url=None, profile_pic_last_modified=None, **kwargs):
        super(User, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic_url = profile_pic_url
        self.profile_pic_last_modified = profile_pic_last_modified

    @classmethod
    def property_mapping(cls):
        mapping = {
            'first_name': 'firstName',
            'last_name': 'lastName',
            'profile_pic_url': 'profilePicUrl',
            'profile_pic_last_modified': 'profilePicLastModified'
        }
        return mapping
