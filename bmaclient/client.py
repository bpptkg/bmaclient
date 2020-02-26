from .bind import bind_method
from .request import OAuth2API

SUPPORTED_FORMATS = ['json']


class MonitoringAPI(OAuth2API):

    host = 'cendana15.com:8080'
    base_path = 'api/v1/'
    protocol = 'http'
    api_name = 'BPPTKG Monitoring API'
    authorize_url = 'http://cendana15.com:8080/oauth/authorize/'
    access_token_url = 'http://cendana15.com:8080/oauth/token/'
    access_token_field = 'access_token'
    redirect_uri = None

    def __init__(self, **kwargs):
        response_format = kwargs.get('format', 'json')
        if response_format in SUPPORTED_FORMATS:
            self.format = response_format
        else:
            raise Exception('Unsupported format')
        self.api_key = kwargs.get('api_key')
        super(MonitoringAPI, self).__init__(**kwargs)

    def get_fetch_method(self, name):
        """Get class fetch method based-on keyword name."""
        method_name = 'fetch_{}'.format(name)
        return getattr(self, method_name, None)

    fetch_doas = bind_method(path='doas/')

    fetch_gas_emission = bind_method(path='gas/emission/')

    fetch_gas_temperature = bind_method(path='gas/temperature/')

    fetch_edm = bind_method(
        path='edm/',
        required_parameters=['benchmark', 'reflector'])

    fetch_gps_position = bind_method(
        path='gps/position/{station}/',
        accepts_parameters=['station'])

    fetch_gps_baseline = bind_method(
        path='gps/baseline/',
        required_parameters=['station1', 'station2'])

    fetch_rsam_seismic = bind_method(
        path='rsam/seismic/{station}/',
        accepts_parameters=['station'])

    fetch_rsam_seismic_band = bind_method(
        path='rsam/seismic/{station}/{band}/',
        accepts_parameters=['station', 'band'])

    fetch_rsam_infrasound = bind_method(
        path='rsam/infrasound/{station}/',
        accepts_parameters=['station'])

    fetch_rsam_infrasound_band = bind_method(
        path='rsam/infrasound/{station}/{band}/',
        accepts_parameters=['station', 'band'])

    fetch_thermal = bind_method(path='thermal/')

    fetch_thermal2 = bind_method(path='thermal2/')

    fetch_tiltmeter = bind_method(
        path='tiltmeter/{station}/',
        accepts_parameters=['station'])

    fetch_tiltmeter_raw = bind_method(
        path='tiltmeter/raw/{station}/',
        accepts_parameters=['station'])

    fetch_tiltborehole = bind_method(
        path='tiltborehole/{station}/',
        accepts_parameters=['station'])

    fetch_seismicity = bind_method(path='seismicity/')

    fetch_bulletin = bind_method(path='bulletin/')

    fetch_energy = bind_method(path='energy/')

    fetch_magnitude = bind_method(path='magnitude/')

    fetch_slope = bind_method(path='slope/')

    slope = bind_method(path='slope/{pk}/',
                        accepts_parameters=['pk'])

    create_slope = bind_method(path='slope/', method='POST')

    replace_slope = bind_method(
        path='slope/{pk}/', method='PUT', accepts_parameters=['pk'])

    update_slope = bind_method(
        path='slope/{pk}/', method='PATCH', accepts_parameters=['pk'])

    delete_slope = bind_method(
        path='slope/{pk}/', method='DELETE', accepts_parameters=['pk'])

    search_slope = bind_method(path='slope/', required_parameters=['search'])

    fetch_users = bind_method(path='users/')

    user = bind_method(path='users/{pk}/', accepts_parameters=['pk'])

    search_users = bind_method(path='users/', required_parameters=['search'])

    fetch_meteorology = bind_method(path='meteorology/')
