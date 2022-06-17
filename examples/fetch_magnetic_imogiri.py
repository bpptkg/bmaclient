from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def main():
    api = MonitoringAPI(api_key=get_api_key())
    data = api.fetch_magnetic_imogiri(
        timestamp__gte="2022-06-10 00:00:00",
        timestamp__lte="2022-06-10 01:00:00",
        nolimit=True,
    )
    print(len(data))


if __name__ == "__main__":
    main()
