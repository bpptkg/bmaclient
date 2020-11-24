import datetime
import time

from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key
from dateutil.parser import parse


def iter_fetch_rsam_seismic(
        start,
        end,
        station,
        sampling='ssam',
        chunk=60,
        verbose=False):
    """
    Fetch RSAM/SSAM data using iter method. This is useful when fetching long
    period of data. Fetching chunk parameter can be provided in minute unit.

    Client API key for credential is automatically read from environment
    variable.

    If verbose is True, print more information about what's going on.

    The overall results is stored as dictionary object.
    """
    def _do_fetch_rsam_seismic(start, end):
        res = client.fetch_rsam_seismic(
            station=station,
            sampling=sampling,
            timestamp__gte=start,
            timestamp__lt=end,
            nolimit=True,
        )
        return res

    client = MonitoringAPI(api_key=get_api_key())
    if isinstance(start, str):
        start = parse(start)
    elif isinstance(start, (datetime.datetime, datetime.date)):
        start = start
    else:
        raise ValueError('Unsupported start value format.')

    if isinstance(end, str):
        end = parse(end)
    elif isinstance(end, (datetime.datetime, datetime.date)):
        end = end
    else:
        raise ValueError('Unsupported end value format')

    results = []

    # Fetch chunk till start less than end.
    i = 0
    while start < end:
        tchunk_start = start
        tchunk_end = start + datetime.timedelta(minutes=chunk)
        if verbose:
            print(f'Fetching chunk {i}, from {tchunk_start} to {tchunk_end}')

        res = _do_fetch_rsam_seismic(tchunk_start, tchunk_end)
        results.extend(res)

        if verbose:
            print('Length response:', len(res))
            print('Length results:', len(results))
        start = tchunk_end
        i += 1

    # Update last chunk.
    if verbose:
        print(f'Fetching last chunk {i}, from {start} to {end}')

    res = _do_fetch_rsam_seismic(start, end)
    results.extend(res)

    if verbose:
        print('Length response:', len(res))
        print('Length results:', len(results))

    return results


if __name__ == '__main__':
    t1 = time.time()

    start = '2020-10-24'
    end = '2020-11-24'
    print(f'Iter fetch RSAM/SSAM data from {start} to {end} ...')

    results = iter_fetch_rsam_seismic(
        start,
        end,
        'pasarbubar',
        verbose=True,
        chunk=24*60,
    )

    print('Length overall results:', len(results))

    t2 = time.time()
    print('Estimated runtime:', t2-t1, 's')
