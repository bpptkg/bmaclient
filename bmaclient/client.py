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
        'This method is used as a legacy to fetch old data. '
        'See more information at: '
        'https://bma.cendana15.com/docs/apis/monitoring/doas.html',
    )(bind_method(
        path='doas/',
        doc='Fetch DOAS data (legacy).'))

    fetch_gas_emission = bind_method(
        path='gas/emission/',
        doc='Fetch Vogamos gas emission data.')

    fetch_gas_temperature = bind_method(
        path='gas/temperature/',
        doc='Fetch Vogamos gas temperature data.')

    fetch_edm = bind_method(
        path='edm/',
        required_parameters=['benchmark', 'reflector'],
        doc='Fetch EDM data.')

    fetch_gps_position = bind_method(
        path='gps/position/{station}/',
        accepts_parameters=['station'],
        doc='Fetch GPS position data.')

    fetch_gps_baseline = bind_method(
        path='gps/baseline/',
        required_parameters=['station1', 'station2'],
        doc='Fetch GPS baseline data.')

    fetch_rsam_seismic = bind_method(
        path='rsam/seismic/{station}/',
        accepts_parameters=['station'],
        doc='Fetch RSAM seismic data.')

    fetch_rsam_seismic_band = bind_method(
        path='rsam/seismic/{station}/{band}/',
        accepts_parameters=['station', 'band'],
        doc='Fetch RSAM seismic band data.')

    fetch_rsam_infrasound = bind_method(
        path='rsam/infrasound/{station}/',
        accepts_parameters=['station'],
        doc='Fetch RSAM infrasound data.')

    fetch_rsam_infrasound_band = bind_method(
        path='rsam/infrasound/{station}/{band}/',
        accepts_parameters=['station', 'band'],
        doc='Fetch RSAM infrasound band data.')

    fetch_thermal = deprecated(
        '0.10.0',
        'fetch_thermal method is deprecated. '
        'Use fetch_thermal2 method instead. '
        'This method is used as a legacy to fetch old data. '
        'See more information at: '
        'https://bma.cendana15.com/docs/apis/monitoring/thermal.html',
    )(bind_method(
        path='thermal/',
        doc='Fetch thermal data (legacy).'))

    fetch_thermal2 = bind_method(
        path='thermal2/',
        doc='Fetch thermal data.')

    fetch_tiltmeter = bind_method(
        path='tiltmeter/{station}/',
        accepts_parameters=['station'],
        doc='Fetch tiltmeter data (filtered from outliers).')

    fetch_tiltmeter_raw = bind_method(
        path='tiltmeter/raw/{station}/',
        accepts_parameters=['station'],
        doc='Fetch raw tiltmeter data (may contains outliers).')

    fetch_tiltborehole = bind_method(
        path='tiltborehole/{station}/',
        accepts_parameters=['station'],
        doc='Fetch tiltmeter borehole data.')

    fetch_tiltmeter_tlr = bind_method(
        path='tiltmeter/tlr/{station}/',
        accepts_parameters=['station'],
        doc='Fetch tiltmeter TLR data.')

    fetch_seismicity = bind_method(
        path='seismicity/',
        doc='Fetch seismicity data.')

    fetch_seismicity_archive = bind_method(
        path='seismicity/archive/',
        doc='Fetch seismicity archive data.')

    fetch_seismicity_cluster = bind_method(
        path='seismicity/cluster/',
        doc='Fetch seismicity cluster data.')

    fetch_bulletin = bind_method(
        path='bulletin/',
        doc='Fetch seismic bulletin data.')

    fetch_energy = bind_method(
        path='energy/',
        doc='Fetch seismic energy data.')

    fetch_magnitude = bind_method(
        path='magnitude/',
        doc='Fetch seismic magnitude data.')

    fetch_slope = bind_method(
        path='slope/',
        doc='Fetch EDM slope distance correction data.')

    slope = bind_method(
        path='slope/{pk}/',
        accepts_parameters=['pk'],
        doc='Fetch EDM slope distance correction data for certain ID.')

    create_slope = bind_method(
        path='slope/',
        method='POST',
        doc='Create EDM slope distance correction.')

    replace_slope = bind_method(
        path='slope/{pk}/',
        method='PUT',
        accepts_parameters=['pk'],
        doc='Replace certain EDM slope distance correction.')

    update_slope = bind_method(
        path='slope/{pk}/',
        method='PATCH',
        accepts_parameters=['pk'],
        doc='Update certain EDM slope distance correction.')

    delete_slope = bind_method(
        path='slope/{pk}/',
        method='DELETE',
        accepts_parameters=['pk'],
        doc='Delete certain EDM slope distance correction.')

    search_slope = bind_method(
        path='slope/',
        required_parameters=['search'],
        doc='Search for EDM slope distance correction.')

    fetch_users = bind_method(
        path='users/',
        doc='Fetch user data.')

    user = bind_method(
        path='users/{pk}/',
        accepts_parameters=['pk'],
        doc='Get info for certain user ID.')

    search_users = bind_method(
        path='users/',
        required_parameters=['search'],
        doc='Search for users.')

    fetch_meteorology = bind_method(
        path='meteorology/',
        doc='Fetch meteorology data.')

    fetch_windrose = bind_method(
        path='meteorology/windrose/',
        doc='Fetch wind rose data.')

    fetch_rainfall = bind_method(
        path='meteorology/rainfall/',
        doc='Fetch rainfall data.')

    fetch_topo = bind_method(
        path='topo/',
        doc='Fetch topography data.')

    fetch_topo_profile = bind_method(
        path='topo/profile/',
        doc='Fetch topography profile data.')

    fetch_doas2 = bind_method(
        path='doas2/{station}/',
        accepts_parameters=['station'],
        doc='Fetch DOAS data.')

    fetch_csdr = bind_method(
        path='edm/csdr/',
        doc='Fetch EDM CSD and rate.')

    fetch_cluster_dict = bind_method(
        path='cluster/dict/',
        doc='Fetch cluster dictionary.')

    fetch_cluster_seisgroup = bind_method(
        path='cluster/seisgroup/',
        doc='Fetch cluster seismicity group.')

    fetch_equivalent_energy = bind_method(
        path='equivalent-energy/',
        doc='Fetch equivalent energy.')

    fetch_lava_domes = bind_method(
        path='lava-domes/',
        required_parameters=['location', 'start', 'end'],
        doc='Fetch lava domes.')

    fetch_rfap_distance = bind_method(
        path='rfap-distance/',
        required_parameters=['start', 'end'],
        doc='Fetch Rockfall-AwanPanas (RF-AP) distance.')
