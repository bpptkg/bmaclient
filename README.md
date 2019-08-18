# bmaclient

BPPTKG Monitoring API Python Client

## Installation

Install from PyPI by typing this command:

    pip install -U bmaclient

Another options is to download archive file from GitLab repository and install
the package:

    tar -xvf bmaclient-v0.1.0.tar.gz
    cd bmaclient-v0.1.0

    pip install -r requirements.txt
    python setup.py install

## Requirements

* Python 3.5+
* httplib2
* six

## Making Requests

You must set valid API key or OAuth2 access token to make authenticated
request. For example, using API key:

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
server resource, It's **recommended** to use OAuth2 access token.

You can apply field lookup filtering by passing keyword arguments:

```python
content = api.fetch_bulletin(eventdate__gte='2019-07-01',
                             eventdate__lt='2019-07-11',
                             eventtype='MP',
                             nolimit=True)
print(content)
```

For the API that requires parameters to be set in the URL path, you can pass
those parameters in the method arguments:

```python
content = api.fetch_tiltmeter(station='selokopo', timestamp__gte='2019-07-01')
print(content)
```

For the API that enable search filtering, you pass `search` keyword in the
method arguments:

```python
content = api.search_slope(search='RB2')
print(content)

content = api.search_users(search='indra')
print(content)
```

## Request Methods

The following URL paths are relative to the base API URL
`http://192.168.5.10/api/v1/`.

|           API Name           |               URL Path               |      Python Method Name      |
| ---------------------------- | ------------------------------------ | ---------------------------- |
| DOAS                         | `/doas/`                             | `fetch_doas`                 |
| EDM                          | `/edm/`                              | `fetch_edm`                  |
| Gas Emission                 | `/gas/emission/`                     | `fetch_gas_emission`         |
| Gas Temperature              | `/gas/temperature/`                  | `fetch_gas_temperature`      |
| GPS Positon                  | `/gps/position/`                     | `fetch_gps_position`         |
| GPS Baseline                 | `/gps/baseline/`                     | `fetch_gps_baseline`         |
| RSAM Seismic                 | `/rsam/seismic/{station}/`           | `fetch_rsam_seismic`         |
| RSAM Seismic Band            | `/rsam/seismic/{station}/{band}/`    | `fetch_rsam_seismic_band`    |
| RSAM Infrasound              | `/rsam/infrasound/{station}/`        | `fetch_rsam_infrasound`      |
| RSAM Infrasound Band         | `/rsam/infrasound/{station}/{band}/` | `fetch_rsam_infrasound_band` |
| Thermal                      | `/thermal/`                          | `fetch_thermal`              |
| Tiltmeter Platform           | `/tiltmeter/{station}/`              | `fetch_tiltmeter`            |
| Tiltmeter Platform Raw       | `/tiltmeter/raw/{station}/`          | `fetch_tiltmeter_raw`        |
| Tiltmeter Borehole           | `/tiltborehole/`                     | `fetch_tiltborehole`         |
| Seismicity                   | `/seismicity`                        | `fetch_seismicity`           |
| Seismic Bulletin             | `/bulletin/`                         | `fetch_bulletin`             |
| Seismic Energy               | `/energy/`                           | `fetch_energy`               |
| Seismic Magnitude            | `/magnitude/`                        | `fetch_magnitude`            |
| EDM Slope Correction         | `/slope/`                            | `fetch_slope`                |
| EDM Slope Correction Detail  | `/slope/{pk}/`                       | `slope`                      |
| Create EDM Slope Correction  | `/slope/`                            | `create_slope`               |
| Replace EDM Slope Correction | `/slope/{pk}/`                       | `replace_slope`              |
| Update EDM Slope Correction  | `/slope/{pk}/`                       | `update_slope`               |
| Search EDM Slope Correction  | `/slope/`                            | `search_slope`               |
| User Profile Info            | `/users/`                            | `fetch_users`                |
| User Detail                  | `/users/{pk}/`                       | `user`                       |
| Search User                  | `/users/`                            | `search_users`               |

For more information about BMA API, see [the BMA API documentation](http://192.168.5.10/docs/).

## Support

This project is maintained by Indra Rudianto. If you have any question about
this project, you can contact him at <indrarudianto.official@gmail.com>.

## Credit

This project is highly inspired by [python-instagram](https://github.com/facebookarchive/python-instagram)
project and use the same design pattern.
The project is licensed under BSD license.
See [LICENSE](https://github.com/Instagram/python-instagram/blob/master/LICENSE.md) for details.

## License

By contributing to the project, you agree that your contributions will be
licensed under its MIT license.
See [LICENSE](https://gitlab.com/bpptkg/bmaclient/blob/master/LICENSE) for details.
