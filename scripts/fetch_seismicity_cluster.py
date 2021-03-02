from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def main():
    api = MonitoringAPI(api_key=get_api_key())
    response = api.fetch_seismicity_cluster(
        eventdate__gte='2021-02-01',
        eventdate__lt='2021-02-10',
        cluster=40,
        nolimit=True,
    )

    print(response)


if __name__ == '__main__':
    main()
