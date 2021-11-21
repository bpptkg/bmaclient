import time

from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def fetch_rsam_seismic(start, end, station, sampling="ssam"):
    client = MonitoringAPI(api_key=get_api_key())
    res = client.fetch_rsam_seismic(
        station=station,
        sampling=sampling,
        timestamp__gte=start,
        timestamp__lt=end,
        nolimit=True,
    )
    return res


if __name__ == "__main__":
    t1 = time.time()

    start = "2020-10-24"
    end = "2020-11-24"
    print(f"Fetch RSAM/SSAM data from {start} to {end} ...")
    results = fetch_rsam_seismic(start, end, "pasarbubar")
    print("Length overall results:", len(results))

    t2 = time.time()
    print("Estimated runtime:", t2 - t1, "s")
