import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selforge.sel700 import SEL700
import unittest
os.system('cls')


class TestSEL700(unittest.TestCase):

    def setUp(self):
        self.relay = SEL700('10.82.125.110', level2=True)

        if self._testMethodName == 'test_edit_wordbit':
            self.relay.edit_wordbit('SET L SV32', 'NA')

        elif self._testMethodName == 'test_close_breaker':
            self.relay.pulse_rb('RB06')
            self.relay.open_breaker()

        elif self._testMethodName == 'test_edit_dnpmap':
            self.relay.edit_dnpmap('BI', 0, 'LT06')

        elif self._testMethodName == 'test_db_on':
            self.relay.test_db('A', 'IA_MAG', '1055')

        elif self._testMethodName == 'test_clear_ser':
            self.relay.clear_ser()


    def test_edit_wordbit(self):
        self.relay.edit_wordbit('SET L SV32', '1 # TESTING SELFORGE')
        self.assertEqual(self.relay.read_wordbit('SHO L SV32'), '1 # TESTING SELFORGE')

    def test_close_breaker(self):
        self.relay.close_breaker()
        self.assertEqual(self.relay.read_target_value('52A'), 1)

    def test_open_breaker(self):
        self.relay.open_breaker()
        self.assertEqual(self.relay.read_target_value('52A'), 0)

    def test_pulse_rb(self):
        self.relay.pulse_rb('RB05')
        self.assertEqual(self.relay.read_target_value('LT03'), 1)

    def test_edit_dnpmap(self):
        self.relay.edit_dnpmap('BI', 0, 'DIRPF')
        self.assertEqual(self.relay.read_dnppoint('BI', 0), 'DIRPF')

    def test_db_on(self):
        self.assertTrue(self.relay.test_db_check())

    def test_db_off(self):
        self.relay.test_db_off()
        self.assertFalse(self.relay.test_db_check())

    def test_read_ser(self):
        ser_reading = self.relay.read_ser()
        if ("Asserted" or "Deasserted") in ser_reading:
            output = True
        else:
            output = False
        self.assertTrue(output)

    def test_clear_ser(self):
        ser_reading = self.relay.read_ser()
        if ("Asserted" or "Deasserted") in ser_reading:
            output = True
        else:
            output = False
        self.assertFalse(output)

    def test_db_overview(self):
        self.relay.test_db('A', 'IA_MAG', '105.40')
        reading = self.relay.test_db_overview()
        if 'IA_MAG' in reading:
            output = True
        else:
            output = False
        self.assertTrue(output)

if __name__ == '__main__':
    unittest.main()
