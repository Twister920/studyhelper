from six import iteritems


class Resource(object):
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self == other

    def to_json(self):
        output_json = {}
        for obj_key, json_key in iteritems(self.property_mapping()):
            attr = getattr(self, obj_key)
            if attr is not None:
                output_json[json_key] = attr
        return output_json

    @classmethod
    def from_json(cls, json):
        mapping = {v: k for k, v in iteritems(cls.property_mapping())}
        return cls(**{mapping[key]: value for key, value in iteritems(json) if key in mapping})

    @classmethod
    def property_mapping(cls):
        """
        A map of property name to json key name for properties that can be simply serialized to/from json
        (no objects, etc.)
        """
        raise NotImplementedError('Resource objects must define a property_mapping')
