# Running the Tests

First, get your API key or access token from BMA server admin, then save it to
the environment variable:

    export API_KEY=YOUR_API_KEY

or

    export ACCESS_TOKEN=YOUR_ACCESS_TOKEN

Make sure BMA server is up and running. Then, run the test for specific module:

    cd /path/to/bmaclient/

    python tests/test_monitor.py
