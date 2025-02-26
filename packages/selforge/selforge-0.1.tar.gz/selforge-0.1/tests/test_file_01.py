import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from selforge.sel700 import SEL700
from datetime import datetime
os.system('cls')


class TestSEL700(unittest.TestCase):

    def setUp(self):
        self.relay = SEL700('10.82.125.110')

    def test_read_wordbit(self):
        self.assertEqual(self.relay.read_wordbit('SHO RID'), 'UCP1 RACK01')

    def test_read_firmware(self):
        self.assertEqual(self.relay.read_firmware(), 'SEL-751-R400-V0-Z100100-D20230315')

    def test_read_part_number(self):
        self.assertEqual(self.relay.read_partnumber(), '751401A1A3A70850830')

    def test_read_serial_number(self):
        self.assertEqual(self.relay.read_serialnumber(), '3231035536')

    def test_read_dnppoint(self):
        self.assertEqual(self.relay.read_dnppoint('BI', 0), 'LT06')

    def test_read_dnpmap(self):
        self.assertTrue(type(self.relay.read_dnpmap()), dict)

    def test_read_target_value(self):
        self.assertEqual(self.relay.read_target_value('ENABLED'), 1)

    def test_read_time(self):
        time_relay = self.relay.read_time()
        time_now = datetime.now().strftime('%H:%M:%S.%f')[:-3]

        time_relay_format = datetime.strptime(time_relay, '%H:%M:%S.%f')
        time_now_format = datetime.strptime(time_now, '%H:%M:%S.%f')
        difference = abs(time_now_format - time_relay_format).total_seconds()*1000
        self.assertLessEqual(difference, 999)

if __name__ == '__main__':
    unittest.main()
