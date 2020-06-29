class ApiModel(object):
    """
    Base API model object.
    """

    @classmethod
    def object_from_dict(cls, entry):
        entry_dict = dict([
            (str(key), value) for key, value in entry.items()
        ])
        return cls(**entry_dict)


class DataModel(object):
    """
    Data model object.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

        self.keys = list(kwargs.keys())

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        if not hasattr(self, key):
            setattr(self, key, value)
            self.keys.append(key)

    def get_keys(self):
        """Get all field keys as list."""
        return self.keys

    def as_dict(self, keys=None):
        """
        Convert the object to dictionary. If keys are provided, it returns
        provided keys with corresponding values. Otherwise returns values with
        default keys.
        """
        keys = keys or self.get_keys()
        if not keys:
            return dict()
        return dict([(key, getattr(self, key)) for key in keys])
