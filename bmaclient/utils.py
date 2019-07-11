from .models import DataModel


def object_from_list(entry):
    """Objectify item in a list of dictionary."""
    return [DataModel(**item) for item in entry]
