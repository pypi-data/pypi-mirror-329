import unittest
from src.barcode_decoder.tme import decode_tme_barcode
from src.barcode_decoder.scanner import CodeType


class TestTMEBarcodeDecoder(unittest.TestCase):
    def test_string_decode(self):
        str1 = 'PDG301-5.0-2P12 1PDG301-5.0-02P-12-00A(H) Q20 K17513107/11'
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '17513107')
        self.assertEqual(decoded.order_number['position'], '11')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'DG301-5.0-2P12')
        self.assertEqual(decoded.mon, 'DG301-5.0-02P-12-00A(H)')
        self.assertEqual(decoded.quantity, 20)
        self.assertEqual(decoded.manufacturer, None)

    def test_string2_decode(self):
        str1 = 'PLP38501TS-ADJ/NOPB 1PLP38501TS-ADJ/NOPB Q4 K16537641/3'
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '16537641')
        self.assertEqual(decoded.order_number['position'], '3')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'LP38501TS-ADJ/NOPB')
        self.assertEqual(decoded.mon, 'LP38501TS-ADJ/NOPB')
        self.assertEqual(decoded.quantity, 4)
        self.assertEqual(decoded.manufacturer, None)

    def test_string3_decode(self):
        str1 = 'PSMAJ15A-13-F 1PSMAJ15A-13-F Q25 4LTW K18098201/1'
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '18098201')
        self.assertEqual(decoded.order_number['position'], '1')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'SMAJ15A-13-F')
        self.assertEqual(decoded.mon, 'SMAJ15A-13-F')
        self.assertEqual(decoded.quantity, 25)
        self.assertEqual(decoded.manufacturer, None)

    def test_string4_decode(self):
        str1 = 'PSMD0402-220K-1% 1P0402WGF2203TCE Q200 K18417297/21'
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '18417297')
        self.assertEqual(decoded.order_number['position'], '21')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'SMD0402-220K-1%')
        self.assertEqual(decoded.mon, '0402WGF2203TCE')
        self.assertEqual(decoded.quantity, 200)
        self.assertEqual(decoded.manufacturer, None)

    def test_string5_decode(self):
        str1 = 'P74HC595PW.118 1P74HC595PW,118 Q25 K18416227/6'
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '18416227')
        self.assertEqual(decoded.order_number['position'], '6')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, '74HC595PW.118')
        self.assertEqual(decoded.mon, '74HC595PW,118')
        self.assertEqual(decoded.quantity, 25)
        self.assertEqual(decoded.manufacturer, None)

    def test_datamatrix_string_no_spaces_decode(self):
        str1 = ('PLAN8720A-CP1PLAN8720A-CPQ5K20835594/3')
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '20835594')
        self.assertEqual(decoded.order_number['position'], '3')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'LAN8720A-CP')
        self.assertEqual(decoded.mon, 'LAN8720A-CP')
        self.assertEqual(decoded.quantity, 5)
        self.assertEqual(decoded.manufacturer, None)

    def test_datamatrix_string2_no_spaces_decode(self):
        str1 = ('PEVE-ER14505/MX221PER14505+MX22-01-1022Q14LCNK51218195/3')
        decoded = decode_tme_barcode(CodeType.DataMatrix, str1)
        self.assertEqual(decoded.order_number['number'], '51218195')
        self.assertEqual(decoded.order_number['position'], '3')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'EVE-ER14505/MX22')
        self.assertEqual(decoded.mon, 'ER14505+MX22-01-1022')
        self.assertEqual(decoded.quantity, 14)
        self.assertEqual(decoded.manufacturer, None)
        self.assertEqual(decoded.coo, 'CN')

    def test_qr_string1_decode(self):
        qr_str = ('QTY:5 PN:LAN8720A-CP PO:30635449/3 MFR:MICROCHIPTECHNOLOGY MPN:LAN8720A-CP RoHS https://www.tme.eu/details/LAN8720A-CP')
        decoded = decode_tme_barcode(CodeType.QR, qr_str)
        self.assertEqual(decoded.order_number['number'], '30635449')
        self.assertEqual(decoded.order_number['position'], '3')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'LAN8720A-CP')
        self.assertEqual(decoded.mon, 'LAN8720A-CP')
        self.assertEqual(decoded.quantity, 5)
        self.assertEqual(decoded.manufacturer, 'MICROCHIPTECHNOLOGY')


if __name__ == '__main__':
    unittest.main()
