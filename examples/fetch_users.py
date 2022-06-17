from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def main():
    api = MonitoringAPI(api_key=get_api_key())
    users = api.fetch_users()
    print(users)


if __name__ == "__main__":
    main()
