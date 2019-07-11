from .bind import bind_method

SUPPORTED_FORMATS = ['json']


class MonitoringAPI(object):

    host = '192.168.5.10'
    base_path = '/api/v1'
    protocol = 'http'
    api_name = 'BPPTKG Monitoring API'

    def __init__(self, **kwargs):
        response_format = kwargs.get('format', 'json')
        if response_format in SUPPORTED_FORMATS:
            self.format = response_format
        else:
            raise Exception('Unsupported format')

    def get_fetch_method(self, name):
        """Get class fetch method based-on keyword name."""
        method_name = 'fetch_{}'.format(name)
        return getattr(self, method_name)

    fetch_doas = bind_method(path='/doas')

    fetch_gas_emission = bind_method(path='/gas/emission')

    fetch_gas_temperature = bind_method(path='/gas/temperature')

    fetch_edm = bind_method(
        path='/edm/',
        required_parameters=['benchmark', 'reflector'])

    fetch_gps_position = bind_method(
        path='/gps/position/{station}',
        accepts_parameters=['station'])

    fetch_gps_baseline = bind_method(
        path='/gps/baseline',
        required_parameters=['station1', 'station2'])

    fetch_rsam_seismic = bind_method(
        path='/rsam/seismic/{station}',
        accepts_parameters=['station'])

    fetch_rsam_seismic_band = bind_method(
        path='/rsam/seismic/{station}/{band}',
        accepts_parameters=['station', 'band'])

    fetch_rsam_infrasound = bind_method(
        path='/rsam/infrasound/{station}',
        accepts_parameters=['station'])

    fetch_rsam_infrasound_band = bind_method(
        path='/rsam/infrasound/{station}/{band}',
        accepts_parameters=['station', 'band'])

    fetch_thermal = bind_method(path='/thermal')

    fetch_tiltmeter = bind_method(
        path='/tiltmeter/{station}',
        accepts_parameters=['station'])

    fetch_tiltmeter_raw = bind_method(
        path='/tiltmeter/raw/{station}',
        accepts_parameters=['station'])

    fetch_tiltborehole = bind_method(
        path='/tiltborehole/{station}',
        accepts_parameters=['station'])

    fetch_seismicity = bind_method(path='/seismicity')

    fetch_bulletin = bind_method(path='/bulletin')

    fetch_energy = bind_method(path='/energy')

    fetch_magnitude = bind_method(path='/magnitude')
