import six


class ApiModel(object):

    @classmethod
    def object_from_dictionary(cls, entry):
        if entry is None:
            return ''
        entry_dict = dict([
            (str(key), value) for key, value in entry.items()
        ])
        return cls(**entry_dict)


class DataModel(ApiModel):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
