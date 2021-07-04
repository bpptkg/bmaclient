# bmaclient

bmaclient is official BPPTKG Monitoring APIs (BMA) Python client. It can be used
to fetch various monitoring data from BMA web services using Python.

## Installation

Install from PyPI by typing this command:

    pip install -U bmaclient

## Making Requests

You must set valid API key or OAuth2 access token to make authenticated request.
For example, using API key:

```python
from bmaclient import MonitoringAPI

api = MonitoringAPI(api_key='API_KEY')
content = api.fetch_bulletin()
print(content)
```

Or using access token:

```python
from bmaclient import MonitoringAPI

api = MonitoringAPI(access_token='ACCESS_TOKEN')
content = api.fetch_bulletin()
print(content)
```

Using API key is only suitable for read only request. If you want to modify
server resources, it's **recommended** to use OAuth2 access token.

You can apply field lookup filtering by passing keyword arguments:

```python
content = api.fetch_bulletin(
    eventdate__gte='2019-07-01 12:24:00',
    eventdate__lt='2019-07-11 13:14:00',
    eventtype='MP',
    nolimit=True
)
print(content)
```

For the APIs that require parameters to be set in the URL path, you can pass
those parameters in the method arguments:

```python
content = api.fetch_tiltmeter(station='selokopo', timestamp__gte='2019-07-01')
print(content)
```

For the APIs that enable search filtering, you pass `search` keyword in the
method arguments:

```python
content = api.search_slope(search='RB2')
print(content)

content = api.search_users(search='indra')
print(content)
```

## Changing the API Host

Starting from version 0.9.0, default API host for the library is
`bma.cendana15.com` and using `https` protocol. If you want to change the host,
for example using other hostname or so, you can write the code as follows:

```python
from bmaclient import MonitoringAPI

api = MonitoringAPI(api_key='API_KEY')
api.host = 'SERVER_ADDRESS'
```

Optionally, change HTTP protocol if the server uses different protocol. Choose
either `http` or `https` protocol:

```python
api = MonitoringAPI(api_key='API_KEY')
api.protocol = 'https'
```

Note that you should include server port if the server doesn't use standard
port. For example:

```python
api.host = 'SERVER_ADDRESS:PORT'
```

## Parameter Encoder

As version 0.10.0, bmaclient adds `bmaclient.encoder.ParameterEncoder` class to
enable using native Python object in the query parameters. Default encoder
supports:

- list, tuple

  It will be encoded to bytes string of comma separated values. For example:

      [1, 2, 3] -> b'1,2,3'
      ['a', 'b', 'c'] -> b'a,b,c'

- str

  str value will be encoded to bytes string. For example:

      'param' -> b'param'

- bytes

  Bytes value will not be touched and returned as it is.

- int, float

  int or float value will be encoded to bytes string. For example:

      12 -> b'12' 14.56 -> b'14.56'

- bool

  Boolean type will be encoded to bytes string with lower case value. For
  example:

      True -> b'true'
      False -> b'false'

- None

  None value will be encoded to empty bytes string. For example:

      None -> b''

- datetime.date

  Date object will be encoded to bytes string of date. Default format is
  `%Y-%m-%d`. For example:

      datetime.date(2020, 1, 1) -> b'2020-01-01'

- datetime.datetime

  Datetime object will be encoded to bytes string of datetime. Default format is
  `%Y-%m-%d %H:%M:%M`. For example:

      datetime.datetime(2020, 1, 1, 9, 46, 12) -> b'2020-01-01 09:46:12'

- other

  Other values will be converted to string with `str` function and encoded with
  ASCII encoding unless default function provided.

Default encoding is ASCII. If you want to use UTF-8 encoding, subclass
ParameterEncoder and set ensure_ascii to False.

Below is an example of subclassing ParameterEncoder class to encode object with
custom type:

```python
import datetime

from bmaclient import MonitoringAPI
from bmaclient.encoder import ParameterEncoder

class GPSStation(object):
    """Custom type."""

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return str(self.code)


class CustomParameterEncoder(ParameterEncoder):
    """Custom parameter encoder."""

    def default(self, o):
        """
        Override default() method to set custom encoder.
        """
        if isinstance(o, GPSStation):
            return str(o).encode('ascii')
        return ParameterEncoder.default(self, o)


api = MonitoringAPI(api_key='API_KEY', encoder_class=CustomParameterEncoder)

pasarbubar = GPSStation('pasarbubar', 'Pasarbubar')
grawah = GPSStation('grawah', 'Grawah')
now = datetime.datetime.now()
onemonthago = now - datetime.timedelta(days=30)

content = api.fetch_gps_baseline(
    station1=pasarbubar,
    station2=grawah,
    timestamp__gte=onemonthago,
    timestamp__lt=now,
    nolimit=True,
)
print(content)
```

## Extending API Class

If you want to extend API class, for example fetching new endpoint that the
method in the library is not available yet, you can see the following example:

```python
from bmaclient import MonitoringAPI
from bmaclient.bind import bind_method


class MyMonitoringAPI(MonitoringAPI):

  def __init__(self, **kwargs):
    super(MyMonitoringAPI, self).__init__(**kwargs)

  fetch_gps_baseline = bind_method(
      path='gps/baseline/',
      required_parameters=['station1', 'station2'],
      doc='Fetch GPS baseline data.')

  fetch_rsam_seismic = bind_method(
      path='rsam/seismic/{station}/',
      accepts_parameters=['station'],
      doc='Fetch RSAM seismic data.')

  fetch_cluster_dict = bind_method(
      path='cluster/dict/',
      doc='Fetch cluster dictionary.')
```

## Request Methods

The following URL paths are relative to the base API URL
`https://bma.cendana15.com/api/v1/`.

|                   API Name                    |               URL Path               |      Python Method Name      |
| --------------------------------------------- | ------------------------------------ | ---------------------------- |
| Cluster Dictionary                            | `/cluster/dict/`                     | `fetch_cluster_dict`         |
| Cluster Seismicity Group                      | `/cluster/seisgroup/`                | `fetch_cluster_seisgroup`    |
| DOAS (`deprecated since v0.10.0`)             | `/doas/`                             | `fetch_doas`                 |
| DOAS v2                                       | `/doas2/{station}/`                  | `fetch_doas2`                |
| EDM                                           | `/edm/`                              | `fetch_edm`                  |
| EDM CSD and Rate                              | `/edm/csdr/`                         | `fetch_csdr`                 |
| Equivalent Energy (`since v0.12.0`)           | `/equivalent-energy/`                | `fetch_equivalent_energy`    |
| Gas Emission                                  | `/gas/emission/`                     | `fetch_gas_emission`         |
| Gas Temperature                               | `/gas/temperature/`                  | `fetch_gas_temperature`      |
| GPS Position                                  | `/gps/position/`                     | `fetch_gps_position`         |
| GPS Baseline                                  | `/gps/baseline/`                     | `fetch_gps_baseline`         |
| Lava Domes (`since v0.13.0`)                  | `/lava-domes/`                       | `fetch_lava_domes`           |
| Meteorology                                   | `/meteorology/`                      | `fetch_meteorology`          |
| Pasarbubar Rainfall                           | `/meteorology/rainfall/`             | `fetch_rainfall`             |
| Pasarbubar Wind Rose                          | `/meteorology/windrose/`             | `fetch_windrose`             |
| Rockfall-AwanPanas Distance (`since v0.13.0`) | `/rfap-distance/`                    | `fetch_rfap_distance`        |
| RSAM Seismic                                  | `/rsam/seismic/{station}/`           | `fetch_rsam_seismic`         |
| RSAM Seismic Band                             | `/rsam/seismic/{station}/{band}/`    | `fetch_rsam_seismic_band`    |
| RSAM Infrasound                               | `/rsam/infrasound/{station}/`        | `fetch_rsam_infrasound`      |
| RSAM Infrasound Band                          | `/rsam/infrasound/{station}/{band}/` | `fetch_rsam_infrasound_band` |
| Thermal (`deprecated since v0.10.0`)          | `/thermal/`                          | `fetch_thermal`              |
| Thermal v2                                    | `/thermal2/`                         | `fetch_thermal2`             |
| Tiltmeter Platform                            | `/tiltmeter/{station}/`              | `fetch_tiltmeter`            |
| Tiltmeter Platform Raw                        | `/tiltmeter/raw/{station}/`          | `fetch_tiltmeter_raw`        |
| Tiltmeter Borehole                            | `/tiltborehole/{station}/`           | `fetch_tiltborehole`         |
| Tiltmeter TLR                                 | `/tiltmeter/tlr/{station}/`          | `fetch_tiltmeter_tlr`        |
| Topography Data                               | `/topo/`                             | `fetch_topo`                 |
| Topography Profile                            | `/topo/profile/`                     | `fetch_topo_profile`         |
| Seismicity                                    | `/seismicity`                        | `fetch_seismicity`           |
| Seismicity Archive                            | `/seismicity/archive/`               | `fetch_seismicity_archive`   |
| Seismicity Cluster                            | `/seismicity/cluster/`               | `fetch_seismicity_cluster`   |
| Seismic Bulletin                              | `/bulletin/`                         | `fetch_bulletin`             |
| Seismic Energy                                | `/energy/`                           | `fetch_energy`               |
| Seismic Magnitude                             | `/magnitude/`                        | `fetch_magnitude`            |
| EDM Slope Correction                          | `/slope/`                            | `fetch_slope`                |
| EDM Slope Correction Detail                   | `/slope/{pk}/`                       | `slope`                      |
| Create EDM Slope Correction                   | `/slope/`                            | `create_slope`               |
| Replace EDM Slope Correction                  | `/slope/{pk}/`                       | `replace_slope`              |
| Update EDM Slope Correction                   | `/slope/{pk}/`                       | `update_slope`               |
| Search EDM Slope Correction                   | `/slope/`                            | `search_slope`               |
| User Profile Info                             | `/users/`                            | `fetch_users`                |
| User Detail                                   | `/users/{pk}/`                       | `user`                       |
| Search User                                   | `/users/`                            | `search_users`               |

For more information about BMA, see [the BMA
documentation](https://bma.cendana15.com/docs/).

## Support

This project is maintained by Indra Rudianto. If you have any question about
this project, you can contact him at <indrarudianto.official@gmail.com>.

## Bugs Reporting

If you found any bug about this library, you can raise an issue on our GitLab
repository at the following
[link](https://gitlab.com/bpptkg/bmaclient/-/issues).

## License

By contributing to the project, you agree that your contributions will be
licensed under its MIT license. See
[LICENSE](https://gitlab.com/bpptkg/bmaclient/blob/master/LICENSE) for details.
