from .bind import bind_method


class MonitoringAPI(object):

    host = '192.168.5.10'
    base_path = '/api/v1'
    protocol = 'http'
    api_name = 'BPPTKG Monitoring API'

    def __init__(self, *args, **kwargs):
        pass

    def get_fetch_method(name):
        method_name = 'fetch_{}'.format(name)
        return getattr(self, method_name)

    fetch_doas = bind_method(path='/doas')

    fetch_gas_emission = bind_method(path='/gas/emission')

    fetch_gas_temperature = bind_method(path='/gas/temperature')

    fetch_edm = bind_method(
        path='/edm/',
        required_parameters=[
            'benchmark', 'reflector', 'ci', 'start_at', 'end_at'])

    fetch_gps_baseline = bind_method(
        path='/gps/baseline',
        required_parameters=['station1', 'station2'])

    fetch_rsam_seismic = bind_method(
        path='/rsam/seismic/{station}/{band}',
        accepts_parameters=['station', 'band'])

    fetch_rsam_infrasound = bind_method(
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

    fetch_energy = bind_method(path='/energy')

    fetch_magnitude = bind_method(path='/magnitude')
