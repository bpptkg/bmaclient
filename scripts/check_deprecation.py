import warnings

from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def main():
    warnings.simplefilter("always", DeprecationWarning)

    api = MonitoringAPI(api_key=get_api_key())
    api.fetch_doas()


if __name__ == "__main__":
    main()
