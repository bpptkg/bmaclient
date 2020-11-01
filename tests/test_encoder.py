import datetime
import unittest

from bmaclient.encoder import ParameterEncoder


class ParameterEncoderTest(unittest.TestCase):

    def test_encode_date(self):
        encoder = ParameterEncoder()
        self.assertEqual(encoder.encode(
            datetime.date(2020, 1, 1)), b'2020-01-01')
        self.assertEqual(encoder.encode(
            datetime.datetime(2020, 1, 1, 1, 2, 3)), b'2020-01-01 01:02:03')

    def test_encode_iterable(self):
        list_obj = [1, 2, 3]
        tuple_obj = (2, 3, 4)
        encoder = ParameterEncoder()
        self.assertEqual(encoder.encode(list_obj), b'1,2,3')
        self.assertEqual(encoder.encode(tuple_obj), b'2,3,4')

    def test_encode_mix_iterable(self):
        obj = [
            datetime.date(2020, 1, 1),
            datetime.datetime(2020, 1, 2, 12, 14, 15),
        ]
        encoder = ParameterEncoder()
        self.assertEqual(
            encoder.encode(obj),
            b'2020-01-01,2020-01-02 12:14:15',
        )

    def test_encode_number(self):
        encoder = ParameterEncoder()
        self.assertEqual(encoder.encode(144), b'144')
        self.assertEqual(encoder.encode(122.3), b'122.3')

    def test_encode_boolean(self):
        encoder = ParameterEncoder()
        self.assertEqual(encoder.encode(True), b'true')
        self.assertEqual(encoder.encode(False), b'false')

    def test_encode_bytes(self):
        encoder = ParameterEncoder()
        self.assertEqual(encoder.encode(b'true'), b'true')

    def test_encode_nonascii(self):
        encoder = ParameterEncoder(ensure_ascii=False)
        unicode_string = 'pythön!'
        self.assertEqual(encoder.encode(unicode_string), b'pyth\xc3\xb6n!')

    def test_encode_custom_type(self):
        class CustomType(object):
            """Custom type."""

            def __init__(self, value):
                self.value = value

            def __str__(self):
                return str(self.value)

        class CustomParameterEncoder(ParameterEncoder):
            """Custom parameter encoder."""

            def default(self, o):
                if isinstance(o, CustomType):
                    return str(o).encode('ascii')
                return ParameterEncoder.default(self, o)

        encoder = CustomParameterEncoder()
        obj = CustomType(1)
        self.assertEqual(str(obj), '1')
        self.assertEqual(encoder.encode(obj), b'1')

        # This should raises an exception as default encoder doesn't handle
        # CustomType object.
        default_encoder = ParameterEncoder()
        with self.assertRaises(TypeError):
            default_encoder.encode(obj)


if __name__ == '__main__':
    unittest.main()
