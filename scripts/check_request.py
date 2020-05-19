"""
Check request to the production server if any error occurred.

How to run:

    $ export API_KEY=YOUR_API_KEY
    $ python scripts/check_request.py
"""

from bmaclient import MonitoringAPI
from bmaclient.utils import get_api_key


def main():
    print('Checking request...')
    api = MonitoringAPI(api_key=get_api_key())

    print('Running: fetch_bulletin')
    api.fetch_bulletin()
    print('Running: fetch_bulletin:page')
    api.fetch_bulletin(page=1)

    print('Running: fetch_doas')
    api.fetch_doas()
    print('Running: fetch_doas:page')
    api.fetch_doas(page=1)

    print('Running: fetch_edm')
    api.fetch_edm(benchmark='BAB0', reflector='RB2')
    print('Running: fetch_edm:page')
    api.fetch_edm(benchmark='BAB0', reflector='RB2', page=1)

    print('Running: fetch_energy')
    api.fetch_energy()
    print('Running: fetch_energy:page')
    api.fetch_energy(page=1)

    print('Running: fetch_gas_emission')
    api.fetch_gas_emission()
    print('Running: fetch_gas_emission:page')
    api.fetch_gas_emission(page=1)

    print('Running: fetch_gas_temperature')
    api.fetch_gas_temperature()
    print('Running: fetch_gas_temperature:page')
    api.fetch_gas_temperature(page=1)

    print('Running: fetch_gps_baseline')
    api.fetch_gps_baseline(station1='klatakan', station2='selo')
    print('Running: fetch_gps_baseline:page')
    api.fetch_gps_baseline(station1='klatakan', station2='selo', page=1)

    print('Running: fetch_gps_position')
    api.fetch_gps_position(station='klatakan')
    print('Running: fetch_gps_position:page')
    api.fetch_gps_position(station='klatakan', page=1)

    print('Running: fetch_magnitude')
    api.fetch_magnitude()
    print('Running: fetch_magnitude:page')
    api.fetch_magnitude(page=1)

    print('Running: fetch_meteorology')
    api.fetch_meteorology()
    print('Running: fetch_meteorology:page')
    api.fetch_meteorology(page=1)

    print('Running: fetch_rsam_infrasound')
    api.fetch_rsam_infrasound(station='kendit')
    print('Running: fetch_rsam_infrasound:page')
    api.fetch_rsam_infrasound(station='kendit', page=1)

    print('Running: fetch_rsam_infrasound_band')
    api.fetch_rsam_infrasound_band(station='kendit', band='band3')
    print('Running: fetch_rsam_infrasound_band:page')
    api.fetch_rsam_infrasound_band(station='kendit', band='band3', page=1)

    print('Running: fetch_rsam_seismic')
    api.fetch_rsam_seismic(station='kendit')
    print('Running: fetch_rsam_seismic:page')
    api.fetch_rsam_seismic(station='kendit', page=1)

    print('Running: fetch_rsam_seismic_band')
    api.fetch_rsam_seismic_band(station='kendit', band='band3')
    print('Running: fetch_rsam_seismic_band:page')
    api.fetch_rsam_seismic_band(station='kendit', band='band3', page=1)

    print('Running: fetch_seismicity')
    api.fetch_seismicity()
    print('Running: fetch_seismicity:page')
    api.fetch_seismicity(page=1)

    print('Running: fetch_slope')
    api.fetch_slope()
    print('Running: fetch_slope:page')
    api.fetch_slope(page=1)

    print('Running: fetch_thermal')
    api.fetch_thermal()
    print('Running: fetch_thermal:page')
    api.fetch_thermal(page=1)

    print('Running: fetch_thermal2')
    api.fetch_thermal2()
    print('Running: fetch_thermal2:page')
    api.fetch_thermal2(page=1)

    print('Running: fetch_tiltborehole')
    api.fetch_tiltborehole(station='klatakan')
    print('Running: fetch_tiltborehole:page')
    api.fetch_tiltborehole(station='klatakan', page=1)

    print('Running: fetch_tiltmeter')
    api.fetch_tiltmeter(station='selokopo')
    print('Running: fetch_tiltmeter:page')
    api.fetch_tiltmeter(station='selokopo', page=1)

    print('Running: fetch_tiltmeter_raw')
    api.fetch_tiltmeter_raw(station='selokopo')
    print('Running: fetch_tiltmeter_raw:page')
    api.fetch_tiltmeter_raw(station='selokopo', page=1)

    print('Running: fetch_tiltmeter_tlr')
    api.fetch_tiltmeter_tlr(station='babadan')
    print('Running: fetch_tiltmeter_tlr:page')
    api.fetch_tiltmeter_tlr(station='babadan', page=1)

    print('Running: fetch_users')
    api.fetch_users()

    print('All request performed successfully.')


if __name__ == '__main__':
    main()
