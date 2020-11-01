from .bind import bind_method
from .deprecations import deprecated
from .encoder import ParameterEncoder
from .request import OAuth2API

SUPPORTED_FORMATS = ['json', 'object']


class MonitoringAPI(OAuth2API):
    """
    Monitoring API object.

    This class represents an API object where users can fetch any kind of
    monitoring data. In order to grant the request, `api_key` or `access_token`
    field must be provided when creating an instance.
    """

    host = 'bma.cendana15.com'
    base_path = 'api/v1/'
    protocol = 'https'
    api_name = 'BPPTKG Monitoring API'
    authorize_url = 'https://bma.cendana15.com/oauth/authorize/'
    access_token_url = 'https://bma.cendana15.com/oauth/token/'
    access_token_field = 'access_token'
    redirect_uri = None

    def __init__(self, **kwargs):
        response_format = kwargs.get('format', 'json')
        if response_format in SUPPORTED_FORMATS:
            self.format = response_format
        else:
            raise Exception('Unsupported response format. '
                            'Valid formats are: {}.'.format(SUPPORTED_FORMATS))
        self.api_key = kwargs.get('api_key')
        self.encoder_class = kwargs.get('encoder_class', ParameterEncoder)
        super(MonitoringAPI, self).__init__(**kwargs)

    def get_fetch_method(self, name):
        """Get class fetch method based-on keyword name."""
        method_name = 'fetch_{}'.format(name)
        return getattr(self, method_name, None)

    fetch_doas = deprecated(
        '0.10.0',
        'fetch_doas method is deprecated. Use fetch_doas2 method instead. '
        'See more information at: '
        'https://bma.cendana15.com/docs/apis/monitoring/doas.html',
    )(bind_method(path='doas/'))

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

    fetch_thermal = deprecated(
        '0.10.0',
        'fetch_thermal method is deprecated. '
        'Use fetch_thermal2 method instead. '
        'See more information at: '
        'https://bma.cendana15.com/docs/apis/monitoring/thermal.html',
    )(bind_method(path='thermal/'))

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

    fetch_tiltmeter_tlr = bind_method(
        path='tiltmeter/tlr/{station}/',
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

    fetch_windrose = bind_method(path='meteorology/windrose/')

    fetch_rainfall = bind_method(path='meteorology/rainfall/')

    fetch_topo = bind_method(path='topo/')

    fetch_doas2 = bind_method(path='doas2/{station}/',
                              accepts_parameters=['station'])
